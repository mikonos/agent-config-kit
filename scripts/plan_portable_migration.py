#!/usr/bin/env python3
"""Plan a source-first portable Skill migration without changing package files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OMITTED_DIRS = {
    ".cache": "dependency_cache",
    ".git": "local_state",
    ".mypy_cache": "dependency_cache",
    ".pytest_cache": "dependency_cache",
    ".ruff_cache": "dependency_cache",
    ".venv": "dependency_cache",
    "__pycache__": "dependency_cache",
    "node_modules": "dependency_cache",
    "venv": "dependency_cache",
}
TEST_METADATA_PATTERN = re.compile(
    r"(^|/)(?:eval|evals|evaluation|test|tests)\.json$"
)
ASCII_TOKEN = re.compile(r"[A-Za-z0-9_.-]+")
ASCII_PART = re.compile(r"[A-Za-z0-9]+")
CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
PRIVATE_REPLACEMENTS = {
    "private_term_001": "老板",
    "private_term_002": "目标项目",
    "private_term_003": "target-project",
    "private_term_004": "target-project",
    "private_term_005": "target-project",
    "private_term_006": "target-project",
    "private_term_007": "目标项目",
}


class MigrationPlanError(Exception):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def text_digest(value: str) -> str:
    return hashlib.sha256(value.casefold().encode("utf-8")).hexdigest()


def sanitize_text(
    text: str,
    ledger: dict[str, Any],
    *,
    replacements: dict[str, str] = PRIVATE_REPLACEMENTS,
    aliases: dict[str, str] | None = None,
) -> tuple[str, bool]:
    terms = ledger.get("terms")
    if ledger.get("schema_version") != 1 or not isinstance(terms, list):
        raise MigrationPlanError("invalid private-term ledger")
    by_digest: dict[str, tuple[str, str, int]] = {}
    for term in terms:
        if not isinstance(term, dict):
            raise MigrationPlanError("invalid private-term record")
        term_id = term.get("id")
        matcher = term.get("matcher")
        digest = term.get("sha256")
        length = term.get("length")
        if (
            not isinstance(term_id, str)
            or term_id not in replacements
            or matcher not in {"ascii_token", "cjk_substring"}
            or not isinstance(digest, str)
            or not isinstance(length, int)
        ):
            raise MigrationPlanError("invalid private-term record")
        by_digest[digest] = (term_id, matcher, length)
    sanitized = text
    for private_name, public_name in sorted(
        (aliases or {}).items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if (
            not private_name
            or not public_name
            or "\\" in public_name
            or public_name.startswith("/")
            or ".." in PurePosixPath(public_name).parts
        ):
            raise MigrationPlanError("invalid private portable alias")
        sanitized = re.sub(
            portable_alias_pattern(private_name),
            public_name,
            sanitized,
            flags=re.IGNORECASE,
        )
    found: dict[str, str] = {}
    ascii_lengths = sorted(
        {record[2] for record in by_digest.values() if record[1] == "ascii_token"},
        reverse=True,
    )
    for token in ASCII_TOKEN.findall(sanitized):
        candidates = [token, *ASCII_PART.findall(token)]
        for part in ASCII_PART.findall(token):
            for length in ascii_lengths:
                candidates.extend(
                    part[start : start + length]
                    for start in range(max(0, len(part) - length + 1))
                )
        for candidate in candidates:
            record = by_digest.get(text_digest(candidate))
            if record is not None and record[1] == "ascii_token":
                found[candidate] = replacements[record[0]]
    cjk_lengths = sorted(
        {record[2] for record in by_digest.values() if record[1] == "cjk_substring"},
        reverse=True,
    )
    for run in CJK_RUN.findall(sanitized):
        for length in cjk_lengths:
            for start in range(max(0, len(run) - length + 1)):
                candidate = run[start : start + length]
                record = by_digest.get(text_digest(candidate))
                if record is not None and record[1] == "cjk_substring":
                    found[candidate] = replacements[record[0]]
    for candidate in sorted(found, key=len, reverse=True):
        sanitized = sanitized.replace(candidate, found[candidate])
    mac_home = re.compile(re.escape("/" + "Users" + "/") + r"[^/\s\"']+/")
    linux_home = re.compile(re.escape("/" + "home" + "/") + r"[^/\s\"']+/")
    sanitized = mac_home.sub("/path/to/", sanitized)
    sanitized = linux_home.sub("/path/to/", sanitized)
    sanitized = re.sub(
        r"[A-Za-z]:\\\\Users\\\\[^\\\\\s\"']+\\\\",
        r"C:\\path\\to\\",
        sanitized,
    )
    sanitized = sanitized.replace("[" + "TODO", "[" + "TBD")
    return sanitized, sanitized != text


def portable_bytes(
    path: Path,
    ledger: dict[str, Any] | None,
    aliases: dict[str, str] | None = None,
) -> bytes:
    value = path.read_bytes()
    if ledger is None:
        return value
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError:
        return value
    sanitized, _ = sanitize_text(text, ledger, aliases=aliases)
    return sanitized.encode("utf-8")


def executable_bits(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode) & 0o111


def package_generator(relative_skill_path: str, skill: str) -> str | None:
    if (
        skill == "all-skills-router"
        and relative_skill_path == "references/skill-index.json"
    ):
        return "scripts/build_full_router_index.py"
    return None


def safe_relative(value: str, label: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or path.is_absolute()
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise MigrationPlanError(f"unsafe {label}: {value!r}")
    return path


def omission_reason(relative: str, *, is_dir: bool = False) -> str | None:
    path = PurePosixPath(relative)
    if is_dir and path.name in OMITTED_DIRS:
        return OMITTED_DIRS[path.name]
    name = path.name
    if (
        name in {
            ".redskill-installed",
            ".skillkit.json",
            "_meta.json",
            "test-prompts.json",
        }
        or relative == ".clawhub/origin.json"
        or TEST_METADATA_PATTERN.search(relative)
    ):
        return "test_metadata"
    if "NSConflict" in name or ".bak-" in name or name.startswith(
        ("archive-", "backup-")
    ):
        return "recovery_artifact"
    return None


def skill_specific_omission_reason(
    *,
    skill: str,
    pack: str,
    relative: str,
    is_dir: bool,
) -> str | None:
    parts = PurePosixPath(relative).parts
    if skill == "huashu-nuwa" and parts and parts[0] == "examples":
        return "generation_material"
    if (
        skill == "huashu-nuwa"
        and not is_dir
        and PurePosixPath(relative).suffix.lower()
        in {".gif", ".jpeg", ".jpg", ".png", ".webp"}
    ):
        return "generation_material"
    if (
        skill.startswith("jtbd-")
        and parts
        and parts[0] == "examples"
    ):
        return "generation_material"
    if skill == "news-extractor" and parts and parts[0] == "output":
        return "local_state"
    if pack in {
        "generated-domain-perspectives",
        "generated-investing-perspectives",
    } and not (
        skill == "xu-shunying-perspective"
        and relative
        in {
            "references/research/03-expression-dna.md",
            "references/research/06-timeline.md",
        }
    ):
        if parts and parts[0] == "scripts":
            return "generation_material"
        if (
            len(parts) >= 2
            and parts[0] == "references"
            and parts[1]
            in {
                "framework",
                "refinement",
                "regression",
                "research",
                "sources",
                "validation",
            }
        ):
            return "generation_material"
        if (
            len(parts) == 2
            and parts[0] == "references"
            and (
                parts[1] in {"checkpoint-log.md", "synthesis.md"}
                or re.match(r"^[0-9]{8}[_-]", parts[1])
            )
        ):
            return "generation_material"
    if (
        skill == "claude-system-prompt-anatomy"
        and parts
        and (
            parts[:2] == ("references", "research")
            or relative == "references/checkpoint-log.md"
        )
    ):
        return "generation_material"
    return None


def source_files_and_omissions(
    root: Path,
    *,
    skill: str,
    pack: str,
) -> tuple[dict[str, Path], list[dict[str, str]]]:
    if root.is_symlink() or not root.is_dir():
        raise MigrationPlanError(f"source Skill directory is unsafe: {root.name}")
    files: dict[str, Path] = {}
    omissions: list[dict[str, str]] = []
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained_dirs: list[str] = []
        for dirname in sorted(dirnames):
            path = current_path / dirname
            relative = path.relative_to(root).as_posix()
            reason = omission_reason(
                relative,
                is_dir=True,
            ) or skill_specific_omission_reason(
                skill=skill,
                pack=pack,
                relative=relative,
                is_dir=True,
            )
            if reason is not None:
                omissions.append(
                    {
                        "description": (
                            "Exclude a source-side dependency, cache, or local-state "
                            "directory from runtime delivery."
                        ),
                        "reason": reason,
                        "source_path": relative,
                        "source_sha256": sha256_tree(path),
                        "source_type": "directory",
                    }
                )
                continue
            if path.is_symlink():
                raise MigrationPlanError(
                    f"source contains an unclassified directory link: "
                    f"{root.name}/{relative}"
                )
            retained_dirs.append(dirname)
        dirnames[:] = retained_dirs
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            reason = omission_reason(
                relative
            ) or skill_specific_omission_reason(
                skill=skill,
                pack=pack,
                relative=relative,
                is_dir=False,
            )
            if reason is not None:
                if path.is_symlink() or not path.is_file():
                    raise MigrationPlanError(
                        f"omitted source file is unsafe: {root.name}/{relative}"
                    )
                omissions.append(
                    {
                        "description": (
                            "Exclude source-side test, recovery, or local metadata "
                            "from runtime delivery."
                        ),
                        "reason": reason,
                        "source_path": relative,
                        "source_sha256": sha256_file(path),
                        "source_type": "file",
                    }
                )
                continue
            if path.is_symlink() or not path.is_file():
                raise MigrationPlanError(
                    f"source contains an unclassified link or entry: "
                    f"{root.name}/{relative}"
                )
            files[relative] = path
    return files, omissions


def regular_package_files(root: Path) -> dict[str, Path]:
    if not root.exists() and not root.is_symlink():
        return {}
    if root.is_symlink() or not root.is_dir():
        raise MigrationPlanError(f"package Skill directory is unsafe: {root.name}")
    files: dict[str, Path] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise MigrationPlanError(
                f"package contains a link: {root.name}/"
                f"{path.relative_to(root).as_posix()}"
            )
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path
        elif not path.is_dir():
            raise MigrationPlanError(
                f"package contains an unsupported entry: {root.name}/"
                f"{path.relative_to(root).as_posix()}"
            )
    return files


def manifest_skill_map(manifest: dict[str, Any]) -> dict[str, str]:
    packs = manifest.get("skill_packs")
    if manifest.get("schema_version") != 1 or not isinstance(packs, dict):
        raise MigrationPlanError("invalid manifest")
    result: dict[str, str] = {}
    for pack, names in packs.items():
        if not isinstance(pack, str) or not isinstance(names, list):
            raise MigrationPlanError("invalid Skill pack")
        for name in names:
            if not isinstance(name, str) or name in result:
                raise MigrationPlanError(f"invalid manifest Skill: {name}")
            result[name] = pack
    return result


def public_identity(name: str, record: dict[str, Any]) -> tuple[str, dict[str, str]]:
    public_name = record.get("public_name", name)
    aliases = record.get("portable_aliases", {})
    if (
        not isinstance(public_name, str)
        or safe_relative(public_name, f"{name} public_name").parts
        != (public_name,)
        or not isinstance(aliases, dict)
        or any(
            not isinstance(private, str)
            or not isinstance(public, str)
            or not private
            or not public
            for private, public in aliases.items()
        )
    ):
        raise MigrationPlanError(f"invalid portable identity: {name}")
    return public_name, aliases


def portable_relative_path(
    relative: str,
    aliases: dict[str, str],
) -> str:
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
        raise MigrationPlanError("invalid portable reference aliases")
    return aliases


def merge_aliases(
    shared: dict[str, str],
    skill_aliases: dict[str, str],
) -> dict[str, str]:
    result = dict(shared)
    for private, public in skill_aliases.items():
        previous = result.get(private)
        if previous is not None and previous != public:
            raise MigrationPlanError(
                f"conflicting portable alias: {private}"
            )
        result[private] = public
    return result


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
        raise MigrationPlanError("invalid private reviewed derivative catalog")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise MigrationPlanError("invalid private reviewed derivative record")
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
            raise MigrationPlanError("invalid private reviewed derivative record")
        safe_relative(source_skill, "reviewed source_skill")
        safe_relative(source_path, "reviewed source_path")
        safe_relative(packaged_path, "reviewed packaged_path")
        if packaged_path in result:
            raise MigrationPlanError(
                f"duplicate private reviewed derivative: {packaged_path}"
            )
        result[packaged_path] = record
    return result


def build_plan(
    *,
    private_inventory: dict[str, Any],
    manifest: dict[str, Any],
    source_roots: dict[str, Path],
    package_root: Path,
    portable_patches: dict[str, Any],
    privacy_ledger: dict[str, Any] | None = None,
    reviewed_derivatives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skills = private_inventory.get("skills")
    patches = portable_patches.get("patches")
    if (
        private_inventory.get("schema_version") != 1
        or private_inventory.get("sensitivity") != "private_do_not_publish"
        or not isinstance(skills, dict)
        or portable_patches.get("schema_version") != 1
        or not isinstance(patches, list)
    ):
        raise MigrationPlanError("invalid inventory or portable patch catalog")
    packaged = manifest_skill_map(manifest)
    patch_by_path = {
        patch["packaged_path"]: patch
        for patch in patches
        if isinstance(patch, dict) and isinstance(patch.get("packaged_path"), str)
    }
    reviewed_by_path = reviewed_derivative_map(reviewed_derivatives)
    shared_aliases = portable_reference_aliases(private_inventory)
    operations: dict[str, list[dict[str, Any]]] = {
        "add": [],
        "replace": [],
        "delete": [],
        "mode": [],
        "preserve_derivative": [],
        "preserve_reviewed_derivative": [],
        "register_derivative": [],
        "register_generated": [],
    }
    omissions: list[dict[str, Any]] = []
    for name, record in sorted(skills.items()):
        disposition = record.get("disposition") if isinstance(record, dict) else None
        if not isinstance(disposition, dict) or disposition.get("status") != "bundled":
            continue
        if not isinstance(record, dict):
            raise MigrationPlanError(f"invalid private Skill record: {name}")
        public_name, skill_aliases = public_identity(name, record)
        aliases = merge_aliases(shared_aliases, skill_aliases)
        pack = packaged.get(public_name)
        if pack is None:
            raise MigrationPlanError(
                f"bundled Skill is missing from manifest: {public_name}"
            )
        source_label = record.get("selected_source")
        selected_path = record.get("selected_path")
        if not isinstance(source_label, str) or not isinstance(selected_path, str):
            raise MigrationPlanError(f"incomplete selected source: {name}")
        source_root = source_roots.get(source_label)
        if source_root is None:
            raise MigrationPlanError(f"missing source root: {source_label}")
        selected = safe_relative(selected_path, f"{name} selected_path")
        source_dir = source_root.joinpath(*selected.parent.parts)
        package_dir = package_root / "packs" / pack / "skills" / public_name
        raw_source_files, source_omissions = source_files_and_omissions(
            source_dir,
            skill=name,
            pack=pack,
        )
        source_files: dict[str, Path] = {}
        source_paths: dict[str, str] = {}
        for source_relative, source_file in raw_source_files.items():
            portable_relative = portable_relative_path(source_relative, aliases)
            if portable_relative in source_files:
                raise MigrationPlanError(
                    f"portable path collision: {name}/{portable_relative}"
                )
            source_files[portable_relative] = source_file
            source_paths[portable_relative] = source_relative
        package_files = regular_package_files(package_dir)
        for omission in source_omissions:
            omissions.append({"skill": name, **omission})
        for relative in sorted(set(source_files) - set(package_files)):
            source_sha256 = sha256_file(source_files[relative])
            operations["add"].append(
                {
                    "skill": name,
                    "source_path": source_paths[relative],
                    "packaged_path": (
                        package_dir / relative
                    ).relative_to(package_root).as_posix(),
                    "source_sha256": source_sha256,
                    "expected_packaged_sha256": sha256_bytes(
                        portable_bytes(
                            source_files[relative],
                            privacy_ledger,
                            aliases,
                        )
                    ),
                }
            )
        for relative in sorted(set(package_files) - set(source_files)):
            operations["delete"].append(
                {
                    "skill": name,
                    "packaged_path": package_files[relative]
                    .relative_to(package_root)
                    .as_posix(),
                    "packaged_sha256": sha256_file(package_files[relative]),
                }
            )
        for relative in sorted(set(source_files) & set(package_files)):
            source = source_files[relative]
            packaged_file = package_files[relative]
            source_hash = sha256_file(source)
            packaged_hash = sha256_file(packaged_file)
            packaged_path = packaged_file.relative_to(package_root).as_posix()
            if executable_bits(source) != executable_bits(packaged_file):
                operations["mode"].append(
                    {
                        "skill": name,
                        "packaged_path": packaged_path,
                        "source_mode": executable_bits(source),
                        "packaged_mode": executable_bits(packaged_file),
                    }
                )
            generator = package_generator(relative, name)
            expected_hash = (
                sha256_bytes(portable_bytes(source, privacy_ledger, aliases))
                if privacy_ledger is not None
                else None
            )
            patch = patch_by_path.get(packaged_path)
            reviewed = reviewed_by_path.get(packaged_path)
            if (
                source_hash != packaged_hash
                and reviewed is not None
                and reviewed.get("source_skill") == name
                and reviewed.get("source_path") == source_paths[relative]
                and reviewed.get("source_sha256") == source_hash
                and reviewed.get("packaged_sha256") == packaged_hash
            ):
                operations["preserve_reviewed_derivative"].append(
                    {
                        "skill": name,
                        "source_path": source_paths[relative],
                        "packaged_path": packaged_path,
                        "source_sha256": source_hash,
                        "packaged_sha256": packaged_hash,
                        "description": reviewed["description"],
                        "reviewed_manual": True,
                    }
                )
                continue
            if (
                source_hash != packaged_hash
                and patch is not None
                and patch.get("source_sha256") == source_hash
                and patch.get("packaged_sha256") == packaged_hash
            ):
                operation = {
                    "skill": name,
                    "source_path": source_paths[relative],
                    "packaged_path": packaged_path,
                    "source_sha256": source_hash,
                    "packaged_sha256": packaged_hash,
                }
                if patch.get("source_snapshot") == (
                    "catalog/maintainer_source_snapshot.json"
                ):
                    if generator is not None:
                        operation["package_generator"] = generator
                    elif expected_hash == packaged_hash:
                        operation["expected_packaged_sha256"] = expected_hash
                    else:
                        operation["expected_packaged_sha256"] = expected_hash
                        operations["replace"].append(operation)
                        continue
                operations["preserve_derivative"].append(operation)
                continue
            if generator is not None and source_hash != packaged_hash:
                operation = {
                    "skill": name,
                    "source_path": source_paths[relative],
                    "packaged_path": packaged_path,
                    "source_sha256": source_hash,
                    "packaged_sha256": packaged_hash,
                    "package_generator": generator,
                }
                operations["register_generated"].append(operation)
                continue
            if privacy_ledger is not None:
                operation = {
                    "skill": name,
                    "source_path": source_paths[relative],
                    "packaged_path": packaged_path,
                    "source_sha256": source_hash,
                    "packaged_sha256": packaged_hash,
                    "expected_packaged_sha256": expected_hash,
                }
                if packaged_hash != expected_hash:
                    operations["replace"].append(operation)
                elif source_hash == packaged_hash:
                    continue
                else:
                    operations["register_derivative"].append(operation)
                continue
            if source_hash == packaged_hash:
                continue
            patch = patch_by_path.get(packaged_path)
            operation = {
                "skill": name,
                "source_path": source_paths[relative],
                "packaged_path": packaged_path,
                "source_sha256": source_hash,
                "packaged_sha256": packaged_hash,
            }
            if (
                patch is not None
                and patch.get("source_sha256") == source_hash
                and patch.get("packaged_sha256") == packaged_hash
            ):
                operations["preserve_derivative"].append(operation)
            else:
                operations["replace"].append(operation)
    summary = Counter({key: len(value) for key, value in operations.items()})
    summary["omit"] = len(omissions)
    return {
        "schema_version": 1,
        "sensitivity": "private_do_not_publish",
        "summary": dict(sorted(summary.items())),
        "operations": operations,
        "omissions": omissions,
    }


def apply_plan(
    *,
    plan: dict[str, Any],
    private_inventory: dict[str, Any],
    source_roots: dict[str, Path],
    package_root: Path,
    privacy_ledger: dict[str, Any] | None = None,
) -> None:
    skills = private_inventory.get("skills")
    operations = plan.get("operations")
    if not isinstance(skills, dict) or not isinstance(operations, dict):
        raise MigrationPlanError("invalid migration plan")
    shared_aliases = portable_reference_aliases(private_inventory)

    def source_for(operation: dict[str, Any]) -> Path:
        record = skills.get(operation.get("skill"))
        if not isinstance(record, dict):
            raise MigrationPlanError("migration operation has an unknown Skill")
        label = record.get("selected_source")
        selected_path = record.get("selected_path")
        relative = operation.get("source_path")
        if (
            not isinstance(label, str)
            or not isinstance(selected_path, str)
            or not isinstance(relative, str)
            or label not in source_roots
        ):
            raise MigrationPlanError("migration operation has an invalid source")
        selected = safe_relative(selected_path, "selected_path")
        source_relative = safe_relative(relative, "source_path")
        return source_roots[label].joinpath(
            *selected.parent.parts,
            *source_relative.parts,
        )

    def target_for(operation: dict[str, Any]) -> Path:
        relative = operation.get("packaged_path")
        if not isinstance(relative, str):
            raise MigrationPlanError("migration operation has no packaged_path")
        safe = safe_relative(relative, "packaged_path")
        return package_root.joinpath(*safe.parts)

    for operation in operations.get("delete", []):
        target = target_for(operation)
        if (
            not target.is_file()
            or target.is_symlink()
            or sha256_file(target) != operation.get("packaged_sha256")
        ):
            raise MigrationPlanError(
                f"delete target changed: {operation.get('packaged_path')}"
            )
    for kind in ("add", "replace"):
        for operation in operations.get(kind, []):
            source = source_for(operation)
            target = target_for(operation)
            if (
                not source.is_file()
                or source.is_symlink()
                or sha256_file(source) != operation.get("source_sha256")
            ):
                raise MigrationPlanError(
                    f"source changed: {operation.get('skill')}/"
                    f"{operation.get('source_path')}"
                )
            if kind == "add" and target.exists():
                raise MigrationPlanError(
                    f"add target already exists: {operation.get('packaged_path')}"
                )
            if kind == "replace" and (
                not target.is_file()
                or target.is_symlink()
                or sha256_file(target) != operation.get("packaged_sha256")
            ):
                raise MigrationPlanError(
                    f"replace target changed: {operation.get('packaged_path')}"
                )

    for operation in operations.get("mode", []):
        target = target_for(operation)
        if not target.is_file() or target.is_symlink():
            raise MigrationPlanError(
                f"mode target changed: {operation.get('packaged_path')}"
            )

    # Materialize and validate all new bytes before changing the package tree.
    # Deletions are committed last so generation failures cannot leave a
    # half-deleted migration.
    with tempfile.TemporaryDirectory(
        dir=package_root.parent,
        prefix=".agent-config-kit-stage-",
    ) as temporary:
        stage_root = Path(temporary)
        staged: list[tuple[Path, Path]] = []
        for kind in ("add", "replace"):
            for operation in operations.get(kind, []):
                source = source_for(operation)
                target = target_for(operation)
                staged_path = stage_root.joinpath(
                    *safe_relative(
                        operation["packaged_path"], "packaged_path"
                    ).parts
                )
                staged_path.parent.mkdir(parents=True, exist_ok=True)
                record = skills[operation["skill"]]
                _, skill_aliases = public_identity(operation["skill"], record)
                aliases = merge_aliases(shared_aliases, skill_aliases)
                staged_path.write_bytes(
                    portable_bytes(source, privacy_ledger, aliases)
                )
                shutil.copymode(source, staged_path)
                expected = operation.get("expected_packaged_sha256")
                if expected is not None and sha256_file(staged_path) != expected:
                    raise MigrationPlanError(
                        f"staged output differs: {operation['packaged_path']}"
                    )
                staged.append((staged_path, target))

        for staged_path, target in staged:
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_path, target)
        for operation in operations.get("mode", []):
            target = target_for(operation)
            current_mode = stat.S_IMODE(target.stat().st_mode)
            os.chmod(
                target,
                (current_mode & ~0o111) | int(operation.get("source_mode", 0)),
            )
        for operation in operations.get("delete", []):
            target_for(operation).unlink()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise MigrationPlanError(f"expected JSON object: {path.name}")
    return value


def parse_source(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must use LABEL=PATH")
    label, raw_path = value.split("=", 1)
    path = Path(raw_path).expanduser().resolve()
    if not label or not path.is_dir():
        raise argparse.ArgumentTypeError("source must use an existing LABEL=PATH")
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
    parser.add_argument("--package-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--privacy-ledger",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "private-term-hashes.json",
    )
    parser.add_argument(
        "--reviewed-derivatives",
        type=Path,
        default=ROOT
        / ".agent-config-kit-workbench"
        / "reviewed-portable-derivatives.json",
    )
    args = parser.parse_args()
    try:
        source_roots = dict(args.source)
        if len(source_roots) != len(args.source):
            raise MigrationPlanError("duplicate source label")
        privacy_ledger = load_object(args.privacy_ledger)
        reviewed_derivatives = load_object(args.reviewed_derivatives)
        plan = build_plan(
            private_inventory=load_object(args.private_inventory),
            manifest=load_object(args.manifest),
            source_roots=source_roots,
            package_root=args.package_root.resolve(),
            portable_patches=load_object(args.portable_patches),
            privacy_ledger=privacy_ledger,
            reviewed_derivatives=reviewed_derivatives,
        )
        if args.apply:
            apply_plan(
                plan=plan,
                private_inventory=load_object(args.private_inventory),
                source_roots=source_roots,
                package_root=args.package_root.resolve(),
                privacy_ledger=privacy_ledger,
            )
    except (MigrationPlanError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"PORTABLE MIGRATION PLAN FAILED: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        counts = " ".join(
            f"{key}={value}" for key, value in plan["summary"].items()
        )
        print(f"PORTABLE MIGRATION PLAN OK: {counts}")
        print("Mode: apply" if args.apply else "Mode: dry-run (no files changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
