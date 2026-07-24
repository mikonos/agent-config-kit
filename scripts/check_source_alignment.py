#!/usr/bin/env python3
"""Fail release when packaged Skills do not match their selected live sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRIORITY = {
    "cursor-vault": 0,
    "agents-global": 1,
    "codex-global": 2,
}
PORTABLE_OMISSION_REASONS = {
    "dependency_cache",
    "generation_material",
    "local_state",
    "recovery_artifact",
    "test_metadata",
}


class AlignmentError(Exception):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value: str, label: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise AlignmentError(f"unsafe {label}: {value!r}")
    return path


def skill_pack_map(manifest: dict[str, Any]) -> dict[str, str]:
    packs = manifest.get("skill_packs")
    if manifest.get("schema_version") != 1 or not isinstance(packs, dict):
        raise AlignmentError("invalid manifest")
    result: dict[str, str] = {}
    for pack, names in packs.items():
        if not isinstance(pack, str) or not isinstance(names, list):
            raise AlignmentError("invalid Skill pack")
        for name in names:
            if not isinstance(name, str) or name in result:
                raise AlignmentError(f"invalid or duplicate packaged Skill: {name}")
            result[name] = pack
    return result


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for current, dirnames, filenames in os.walk(path, followlinks=False):
        current_path = Path(current)
        dirnames.sort()
        filenames.sort()
        for dirname in dirnames:
            child = current_path / dirname
            relative = child.relative_to(path).as_posix()
            digest.update(f"dir:{relative}\0".encode("utf-8"))
            if child.is_symlink():
                digest.update(f"link:{os.readlink(child)}\0".encode("utf-8"))
        for filename in filenames:
            child = current_path / filename
            relative = child.relative_to(path).as_posix()
            if child.is_symlink():
                digest.update(
                    f"symlink:{relative}:{os.readlink(child)}\0".encode("utf-8")
                )
            else:
                digest.update(f"file:{relative}\0".encode("utf-8"))
                digest.update(child.read_bytes())
                digest.update(b"\0")
    return digest.hexdigest()


def regular_files(
    root: Path,
    *,
    excluded_directories: set[str] | None = None,
) -> dict[str, Path]:
    if root.is_symlink() or not root.is_dir():
        raise AlignmentError(f"Skill directory is missing or unsafe: {root.name}")
    excluded = excluded_directories or set()
    result: dict[str, Path] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for dirname in sorted(dirnames):
            path = current_path / dirname
            relative = path.relative_to(root).as_posix()
            if relative in excluded:
                continue
            if path.is_symlink():
                raise AlignmentError(
                    f"Skill contains a link: {root.name}/{relative}"
                )
            retained.append(dirname)
        dirnames[:] = retained
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.is_file():
                raise AlignmentError(
                    f"Skill contains an unsupported entry: {root.name}/{relative}"
                )
            result[relative] = path
    return result


def executable_bits(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode) & 0o111


def public_skill_name(name: str, record: dict[str, Any]) -> str:
    public_name = record.get("public_name", name)
    if (
        not isinstance(public_name, str)
        or safe_relative(public_name, f"{name} public_name").parts
        != (public_name,)
    ):
        raise AlignmentError(f"invalid public Skill name: {name}")
    return public_name


def portable_aliases(name: str, record: dict[str, Any]) -> dict[str, str]:
    aliases = record.get("portable_aliases", {})
    if (
        not isinstance(aliases, dict)
        or any(
            not isinstance(private, str)
            or not isinstance(public, str)
            or not private
            or not public
            or "/" in public
            or "\\" in public
            for private, public in aliases.items()
        )
    ):
        raise AlignmentError(f"invalid portable aliases: {name}")
    return aliases


def portable_relative_path(relative: str, aliases: dict[str, str]) -> str:
    portable = relative
    for private_name, public_name in sorted(
        aliases.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        portable = re.sub(
            portable_alias_pattern(private_name),
            public_name,
            portable,
            flags=re.IGNORECASE,
        )
    return safe_relative(portable, "portable relative path").as_posix()


def portable_alias_pattern(private_name: str) -> str:
    escaped = re.escape(private_name)
    if re.fullmatch(r"_[A-Za-z0-9]+", private_name):
        return rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])"
    return escaped


def portable_reference_aliases(
    private_inventory: dict[str, Any],
) -> dict[str, str]:
    aliases = private_inventory.get("portable_reference_aliases", {})
    if (
        not isinstance(aliases, dict)
        or any(
            not isinstance(private, str)
            or not isinstance(public, str)
            or not private
            or not public
            or "\\" in public
            or public.startswith("/")
            or ".." in PurePosixPath(public).parts
            for private, public in aliases.items()
        )
    ):
        raise AlignmentError("invalid portable reference aliases")
    return aliases


def merge_aliases(
    shared: dict[str, str],
    skill_aliases: dict[str, str],
) -> dict[str, str]:
    result = dict(shared)
    for private, public in skill_aliases.items():
        previous = result.get(private)
        if previous is not None and previous != public:
            raise AlignmentError(f"conflicting portable alias: {private}")
        result[private] = public
    return result


def transformation_maps(
    portable_patches: dict[str, Any],
    private_omissions: dict[str, Any] | None = None,
) -> tuple[
    dict[str, dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
]:
    patches = portable_patches.get("patches")
    omissions = list(portable_patches.get("omissions", []))
    if (
        portable_patches.get("schema_version") != 1
        or not isinstance(patches, list)
        or not isinstance(omissions, list)
    ):
        raise AlignmentError("invalid portable patch catalog")
    if private_omissions is not None:
        private_entries = private_omissions.get("omissions")
        if (
            private_omissions.get("schema_version") != 1
            or private_omissions.get("sensitivity")
            != "private_do_not_publish"
            or not isinstance(private_entries, list)
        ):
            raise AlignmentError("invalid private portable omission catalog")
        omissions.extend(private_entries)
    patch_result: dict[str, dict[str, Any]] = {}
    for patch in patches:
        packaged_path = patch.get("packaged_path") if isinstance(patch, dict) else None
        if not isinstance(packaged_path, str):
            raise AlignmentError("portable patch is missing packaged_path")
        safe_relative(packaged_path, "packaged_path")
        if packaged_path in patch_result:
            raise AlignmentError(f"duplicate portable patch: {packaged_path}")
        patch_result[packaged_path] = patch
    omission_result: dict[tuple[str, str], dict[str, Any]] = {}
    for omission in omissions:
        if not isinstance(omission, dict):
            raise AlignmentError("portable omission entry must be an object")
        skill = omission.get("skill")
        source_path = omission.get("source_path")
        if not isinstance(skill, str) or not isinstance(source_path, str):
            raise AlignmentError("portable omission is missing skill or source_path")
        safe_relative(skill, "omission skill")
        safe_relative(source_path, "omission source_path")
        key = (skill, source_path)
        if key in omission_result:
            raise AlignmentError(f"duplicate portable omission: {skill}/{source_path}")
        omission_result[key] = omission
    return patch_result, omission_result


def reviewed_derivative_map(
    catalog: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    if catalog is None:
        return {}
    records = catalog.get("derivatives")
    if (
        catalog.get("schema_version") != 1
        or catalog.get("sensitivity") != "private_do_not_publish"
        or not isinstance(records, list)
    ):
        raise AlignmentError("invalid private reviewed derivative catalog")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise AlignmentError("invalid private reviewed derivative record")
        source_skill = record.get("source_skill")
        source_path = record.get("source_path")
        packaged_path = record.get("packaged_path")
        source_sha256 = record.get("source_sha256")
        packaged_sha256 = record.get("packaged_sha256")
        description = record.get("description")
        if (
            not isinstance(source_skill, str)
            or not isinstance(source_path, str)
            or not isinstance(packaged_path, str)
            or not isinstance(source_sha256, str)
            or len(source_sha256) != 64
            or not isinstance(packaged_sha256, str)
            or len(packaged_sha256) != 64
            or not isinstance(description, str)
            or not description.strip()
        ):
            raise AlignmentError("invalid private reviewed derivative record")
        safe_relative(source_skill, "reviewed source_skill")
        safe_relative(source_path, "reviewed source_path")
        safe_relative(packaged_path, "reviewed packaged_path")
        if packaged_path in result:
            raise AlignmentError(
                f"duplicate private reviewed derivative: {packaged_path}"
            )
        result[packaged_path] = record
    return result


def read_skill_name(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8", errors="ignore")[:8000]
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
    return match.group(1).strip() if match else skill_file.parent.name


def discover_live_sources(
    source_roots: dict[str, Path],
) -> dict[str, list[tuple[str, str]]]:
    candidates: dict[str, list[tuple[str, str]]] = {}
    for label, root in source_roots.items():
        for skill_file in sorted(root.glob("*/SKILL.md")):
            if skill_file.is_symlink() or skill_file.parent.is_symlink():
                raise AlignmentError(
                    f"top-level Skill source is a link: {skill_file.parent.name}"
                )
            candidates.setdefault(read_skill_name(skill_file), []).append(
                (label, skill_file.relative_to(root).as_posix())
            )
    return {
        name: sorted(
            entries,
            key=lambda entry: (
                SOURCE_PRIORITY.get(entry[0], 99),
                entry[0],
                entry[1],
            ),
        )
        for name, entries in candidates.items()
    }


def compare_skill(
    *,
    source_name: str,
    public_name: str,
    source_dir: Path,
    packaged_dir: Path,
    package_root: Path,
    patches: dict[str, dict[str, Any]],
    omissions: dict[tuple[str, str], dict[str, Any]],
    reviewed_derivatives: dict[str, dict[str, Any]],
    aliases: dict[str, str],
) -> tuple[str, list[str]]:
    directory_omissions = {
        source_path: omission
        for (skill, source_path), omission in omissions.items()
        if skill == source_name and omission.get("source_type") == "directory"
    }
    directory_problems: list[str] = []
    for relative, omission in directory_omissions.items():
        directory = source_dir.joinpath(*PurePosixPath(relative).parts)
        if (
            not directory.is_dir()
            or directory.is_symlink()
            or omission.get("source_sha256") != sha256_tree(directory)
        ):
            directory_problems.append(
                f"{source_name}/{relative}: portable directory omission digest "
                "does not match source"
            )
    raw_source_files = regular_files(
        source_dir,
        excluded_directories=set(directory_omissions),
    )
    source_files: dict[str, Path] = {}
    source_paths: dict[str, str] = {}
    for source_relative, source_file in raw_source_files.items():
        portable_relative = portable_relative_path(source_relative, aliases)
        if portable_relative in source_files:
            raise AlignmentError(
                f"portable path collision: {source_name}/{portable_relative}"
            )
        source_files[portable_relative] = source_file
        source_paths[portable_relative] = source_relative
    packaged_files = regular_files(packaged_dir)
    source_names = set(source_files)
    packaged_names = set(packaged_files)
    missing = sorted(source_names - packaged_names)
    extra = sorted(packaged_names - source_names)
    if extra:
        return (
            "unexplained",
            [
                f"{source_name}: file set differs "
                f"missing={missing} extra={extra}"
            ],
        )

    derived = bool(directory_omissions) or any(
        portable != source_paths[portable]
        for portable in source_files
    )
    problems: list[str] = list(directory_problems)
    omission_paths = {
        source_path
        for (skill, source_path), omission in omissions.items()
        if skill == source_name
        and omission.get("source_type", "file") == "file"
    }
    missing_source_paths = {source_paths[relative] for relative in missing}
    stale_omissions = sorted(omission_paths - missing_source_paths)
    for relative in stale_omissions:
        problems.append(f"{source_name}/{relative}: portable omission is stale")
    for relative in missing:
        source_relative = source_paths[relative]
        omission = omissions.get((source_name, source_relative))
        if omission is None:
            problems.append(
                f"{source_name}/{source_relative}: unregistered source omission"
            )
            continue
        if omission.get("source_sha256") != sha256_file(source_files[relative]):
            problems.append(
                f"{source_name}/{source_relative}: portable omission digest does not match source"
            )
            continue
        if omission.get("reason") not in PORTABLE_OMISSION_REASONS:
            problems.append(
                f"{source_name}/{relative}: invalid portable omission reason"
            )
            continue
        if (
            not isinstance(omission.get("description"), str)
            or not omission["description"].strip()
        ):
            problems.append(
                f"{source_name}/{relative}: incomplete portable omission"
            )
            continue
        derived = True
    for relative in sorted(source_names & packaged_names):
        source = source_files[relative]
        packaged = packaged_files[relative]
        if executable_bits(source) != executable_bits(packaged):
            problems.append(f"{source_name}/{relative}: executable mode differs")
            continue
        source_hash = sha256_file(source)
        packaged_hash = sha256_file(packaged)
        if source_hash == packaged_hash:
            continue
        packaged_path = packaged.relative_to(package_root).as_posix()
        source_relative = source_paths[relative]
        patch = patches.get(packaged_path)
        if patch is None:
            problems.append(
                f"{source_name}/{relative}: unregistered content difference"
            )
            continue
        source_path = patch.get("source_path")
        try:
            safe_source_path = (
                safe_relative(source_path, "source_path")
                if isinstance(source_path, str)
                else None
            )
        except AlignmentError:
            safe_source_path = None
        relative_path = PurePosixPath(source_relative)
        expected_suffix = PurePosixPath(source_name).joinpath(
            relative_path
        ).parts
        maintainer_private = patch.get("source_snapshot") == (
            "catalog/maintainer_source_snapshot.json"
        )
        if not maintainer_private and (
            safe_source_path is None
            or not (
                safe_source_path == relative_path
                or safe_source_path.parts[-len(expected_suffix) :] == expected_suffix
            )
        ):
            problems.append(
                f"{source_name}/{relative}: portable patch source_path does not match "
                "selected Skill"
            )
            continue
        upstream_commit = patch.get("upstream_commit")
        source_snapshot = patch.get("source_snapshot")
        if (upstream_commit is None) == (source_snapshot is None):
            problems.append(
                f"{source_name}/{relative}: portable patch needs exactly one source anchor"
            )
            continue
        if not isinstance(patch.get("upstream_origin"), str) or not patch[
            "upstream_origin"
        ].strip():
            problems.append(
                f"{source_name}/{relative}: portable patch is missing upstream_origin"
            )
            continue
        if not isinstance(patch.get("description"), str) or not patch[
            "description"
        ].strip():
            problems.append(
                f"{source_name}/{relative}: portable patch is missing description"
            )
            continue
        if (
            patch.get("source_sha256") != source_hash
            or patch.get("packaged_sha256") != packaged_hash
        ):
            problems.append(
                f"{source_name}/{relative}: portable patch digest does not match content"
            )
            continue
        if patch.get("transformation") == "reviewed_manual_portable_derivative":
            reviewed = reviewed_derivatives.get(packaged_path)
            if (
                reviewed is None
                or reviewed.get("source_skill") != source_name
                or reviewed.get("source_path") != source_relative
                or reviewed.get("packaged_path") != packaged_path
                or reviewed.get("source_sha256") != source_hash
                or reviewed.get("packaged_sha256") != packaged_hash
            ):
                problems.append(
                    f"{source_name}/{relative}: reviewed derivative lacks exact "
                    "private approval"
                )
                continue
        derived = True
    if problems:
        return "unexplained", problems
    return ("portable_derivative" if derived else "exact"), []


def check_alignment(
    *,
    private_inventory: dict[str, Any],
    manifest: dict[str, Any],
    source_roots: dict[str, Path],
    package_root: Path,
    portable_patches: dict[str, Any],
    private_omissions: dict[str, Any] | None = None,
    private_reviewed_derivatives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skills = private_inventory.get("skills")
    kit_snapshots = private_inventory.get("catalog_only_skills", [])
    if (
        private_inventory.get("schema_version") != 1
        or private_inventory.get("sensitivity") != "private_do_not_publish"
        or not isinstance(skills, dict)
        or not isinstance(kit_snapshots, list)
        or any(not isinstance(name, str) for name in kit_snapshots)
        or len(kit_snapshots) != len(set(kit_snapshots))
    ):
        raise AlignmentError("invalid private Skill inventory")
    kit_snapshot_names = set(kit_snapshots)
    packaged = skill_pack_map(manifest)
    patches, omissions = transformation_maps(
        portable_patches,
        private_omissions,
    )
    reviewed_derivatives = reviewed_derivative_map(
        private_reviewed_derivatives
    )
    shared_aliases = portable_reference_aliases(private_inventory)
    counts: Counter[str] = Counter()
    problems: list[str] = []
    results: dict[str, str] = {}

    live_sources = discover_live_sources(source_roots)
    claimed_public_names: set[str] = set()
    for name in sorted(set(live_sources) - set(skills)):
        results[name] = "unexplained"
        counts["unexplained"] += 1
        problems.append(f"{name}: live source is missing from private inventory")

    for name, record in sorted(skills.items()):
        if not isinstance(name, str) or not isinstance(record, dict):
            raise AlignmentError("invalid private Skill record")
        public_name = public_skill_name(name, record)
        aliases = merge_aliases(
            shared_aliases,
            portable_aliases(name, record),
        )
        if public_name in claimed_public_names:
            raise AlignmentError(f"duplicate public Skill name: {public_name}")
        claimed_public_names.add(public_name)
        selected_source = record.get("selected_source")
        source_candidates = live_sources.get(name, [])
        expected_source = source_candidates[0][0] if source_candidates else None
        if expected_source is not None and selected_source != expected_source:
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(
                f"{name}: selected source is stale "
                f"expected={expected_source} actual={selected_source}"
            )
            continue
        preferred_candidates = [
            candidate
            for candidate in source_candidates
            if candidate[0] == expected_source
        ]
        if len(preferred_candidates) > 1:
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(
                f"{name}: selected source name is ambiguous within {expected_source}"
            )
            continue
        selected_path = record.get("selected_path")
        if (
            preferred_candidates
            and selected_path != preferred_candidates[0][1]
        ):
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(
                f"{name}: selected source path is stale within {expected_source}"
            )
            continue
        disposition = record.get("disposition")
        status = disposition.get("status") if isinstance(disposition, dict) else None
        if status == "blocked":
            if name in packaged:
                results[name] = "unexplained"
                counts["unexplained"] += 1
                problems.append(f"{name}: blocked Skill is still present in manifest")
            else:
                results[name] = "excluded"
                counts["excluded"] += 1
            continue
        if status == "review":
            results[name] = "review"
            counts["review"] += 1
            problems.append(f"{name}: release disposition is still review")
            continue
        if status == "fetch_from_origin":
            if name in packaged:
                results[name] = "unexplained"
                counts["unexplained"] += 1
                problems.append(f"{name}: external Skill is still present in manifest")
            else:
                results[name] = "external"
                counts["external"] += 1
            continue
        if status != "bundled":
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(f"{name}: unsupported release disposition {status!r}")
            continue

        pack = packaged.get(public_name)
        if pack is None:
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(f"{name}: bundled source is missing from manifest")
            continue
        source_label = selected_source
        source_path = selected_path
        if not isinstance(source_label, str) or not isinstance(source_path, str):
            raise AlignmentError(f"{name}: selected source is incomplete")
        source_root = source_roots.get(source_label)
        if source_root is None:
            results[name] = "unexplained"
            counts["unexplained"] += 1
            problems.append(f"{name}: selected source root is unavailable")
            continue
        selected = safe_relative(source_path, f"{name} selected_path")
        source_dir = source_root.joinpath(*selected.parent.parts)
        packaged_dir = package_root / "packs" / pack / "skills" / public_name
        try:
            alignment, skill_problems = compare_skill(
                source_name=name,
                public_name=public_name,
                source_dir=source_dir,
                packaged_dir=packaged_dir,
                package_root=package_root,
                patches=patches,
                omissions=omissions,
                reviewed_derivatives=reviewed_derivatives,
                aliases=aliases,
            )
        except AlignmentError as exc:
            alignment = "unexplained"
            skill_problems = [f"{name}: {exc}"]
        results[name] = alignment
        counts[alignment] += 1
        problems.extend(skill_problems)

    packaged_only = set(packaged) - claimed_public_names
    for name in sorted(packaged_only):
        if name in kit_snapshot_names:
            results[name] = "kit_snapshot"
            counts["kit_snapshot"] += 1
        else:
            results[name] = "catalog_only"
            counts["catalog_only"] += 1
            problems.append(
                f"{name}: packaged Skill is missing from private inventory"
            )
    for name in sorted(kit_snapshot_names - packaged_only):
        counts["unexplained"] += 1
        problems.append(
            f"{name}: private Kit snapshot decision is stale or shadows a live source"
        )

    ordered_counts = {
        key: counts[key]
        for key in (
            "exact",
            "portable_derivative",
            "excluded",
            "review",
            "external",
            "kit_snapshot",
            "catalog_only",
            "unexplained",
        )
    }
    release_ready = (
        counts["review"] == 0
        and counts["catalog_only"] == 0
        and counts["unexplained"] == 0
    )
    return {
        "release_ready": release_ready,
        "counts": ordered_counts,
        "skills": results,
        "problems": problems,
    }


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AlignmentError(f"invalid JSON: {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise AlignmentError(f"expected JSON object: {path.name}")
    return value


def parse_source(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must use LABEL=PATH")
    label, raw_path = value.split("=", 1)
    if not label:
        raise argparse.ArgumentTypeError("source label is empty")
    path = Path(raw_path).expanduser().resolve()
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"source directory does not exist: {raw_path}")
    return label, path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, type=parse_source)
    parser.add_argument("--private-inventory", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=ROOT / "manifest.json")
    parser.add_argument(
        "--portable-patches",
        type=Path,
        default=ROOT / "catalog" / "portable_patches.json",
    )
    parser.add_argument(
        "--private-omissions",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "private-portable-omissions.json",
    )
    parser.add_argument(
        "--private-reviewed-derivatives",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "reviewed-portable-derivatives.json",
    )
    parser.add_argument("--package-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        source_roots = dict(args.source)
        if len(source_roots) != len(args.source):
            raise AlignmentError("duplicate source label")
        report = check_alignment(
            private_inventory=load_object(args.private_inventory),
            manifest=load_object(args.manifest),
            source_roots=source_roots,
            package_root=args.package_root.resolve(),
            portable_patches=load_object(args.portable_patches),
            private_omissions=load_object(args.private_omissions),
            private_reviewed_derivatives=load_object(
                args.private_reviewed_derivatives
            ),
        )
    except (AlignmentError, OSError, KeyError, TypeError) as exc:
        print(f"SOURCE ALIGNMENT FAILED: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        counts = " ".join(f"{key}={value}" for key, value in report["counts"].items())
        print(f"SOURCE ALIGNMENT {'OK' if report['release_ready'] else 'FAILED'}: {counts}")
        for problem in report["problems"]:
            print(f"- {problem}")
    return 0 if report["release_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
