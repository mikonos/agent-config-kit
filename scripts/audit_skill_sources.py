#!/usr/bin/env python3
"""Inventory Skill sources without copying or exposing their contents."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional


EXCLUDED_DIR_NAMES = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".system",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
    "vendor",
}
PLATFORM_BUILTIN_DIR_NAMES = {".system"}
SAFE_BINARY_EXTENSIONS = {
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".otf",
    ".pdf",
    ".png",
    ".ttf",
    ".webp",
    ".woff",
    ".woff2",
}
DANGEROUS_BINARY_EXTENSIONS = {
    ".bin",
    ".class",
    ".dll",
    ".dylib",
    ".exe",
    ".jar",
    ".so",
}
LICENSE_NAMES = {
    "copying",
    "license",
    "license.md",
    "license.txt",
    "notice",
    "notice.md",
    "third_party_notices.md",
}
MAX_TEXT_BYTES = 2_000_000

PERSONAL_PATTERNS = {
    "macos_home_path": re.compile(
        re.escape("/" + "Users" + "/") + r"[^/\s\"'`]+/"
    ),
    "linux_home_path": re.compile(
        re.escape("/" + "home" + "/") + r"[^/\s\"'`]+/"
    ),
    "windows_home_path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s\"'`]+\\"),
}
SECRET_PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "aws_temporary_access_key": re.compile(r"ASIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}"),
    "github_fine_grained_token": re.compile(
        r"github_pat_[A-Za-z0-9_]{20,}"
    ),
    "google_api_key": re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    "openai_style_secret": re.compile(
        r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"
    ),
    "private_key": re.compile(
        r"BEGIN (?:(?:RSA|OPENSSH|EC|DSA|ENCRYPTED) )?PRIVATE KEY"
    ),
    "pgp_private_key": re.compile("BEGIN " + r"PGP PRIVATE KEY BLOCK"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
}
SENSITIVE_CANDIDATE_PATTERNS = {
    "openai_style_secret_candidate": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
}
COMMAND_PATTERNS = {
    command: re.compile(
        rf"(?<![A-Za-z0-9_.-]){re.escape(command)}(?![A-Za-z0-9_.-])",
        re.IGNORECASE,
    )
    for command in (
        "bash",
        "docker",
        "gh",
        "git",
        "node",
        "npm",
        "npx",
        "obsidian",
        "opencli",
        "pip",
        "python",
        "python3",
        "sh",
        "uv",
    )
}
SIDE_EFFECT_PATTERNS = {
    "deletion": re.compile(r"\brm\s+-rf\b|\bunlink\b|\bdelete\b|删除", re.IGNORECASE),
    "deployment_or_publish": re.compile(
        r"\bdeploy(?:ment)?\b|\bpublish\b|部署|发布", re.IGNORECASE
    ),
    "external_message": re.compile(
        r"\bsend(?:ing)?\s+(?:an?\s+)?(?:email|message)\b|发消息|发送邮件",
        re.IGNORECASE,
    ),
    "payment": re.compile(r"\bpayment\b|\bcharge\b|付款|支付", re.IGNORECASE),
}
ENV_PATTERNS = (
    re.compile(r"\$\{([A-Z][A-Z0-9_]{2,})\}"),
    re.compile(r"\$([A-Z][A-Z0-9_]{2,})\b"),
    re.compile(r"process\.env\.([A-Z][A-Z0-9_]{2,})"),
    re.compile(r"os\.environ(?:\.get)?\([\"']([A-Z][A-Z0-9_]{2,})"),
)
PROMPT_PLACEHOLDERS = {"ARGUMENTS"}


def parse_source(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must use LABEL=PATH")
    label, raw_path = value.split("=", 1)
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", label):
        raise argparse.ArgumentTypeError(
            "source label must contain lowercase letters, numbers, hyphens, or underscores"
        )
    path = Path(raw_path).expanduser().resolve()
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"source directory does not exist: {raw_path}")
    return label, path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_frontmatter(text: str) -> tuple[Optional[str], Optional[str]]:
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---", 4)
    if end < 0:
        return None, None
    frontmatter = text[4:end]
    name_match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", frontmatter)
    license_match = re.search(r"(?m)^license:\s*[\"']?([^\n\"']+)", frontmatter)
    name = name_match.group(1).strip() if name_match else None
    license_name = license_match.group(1).strip() if license_match else None
    return name, license_name


def nearest_skill_dir(path: Path, skill_dirs: set[Path]) -> Optional[Path]:
    current = path.parent
    while True:
        if current in skill_dirs:
            return current
        if current == current.parent:
            return None
        current = current.parent


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def is_link_or_reparse(path: Path) -> bool:
    try:
        metadata = path.lstat()
    except OSError:
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & reparse_flag)


def is_backup_artifact(name: str) -> bool:
    lowered = name.lower()
    return (
        "nsconflict" in lowered
        or lowered.endswith(("~", ".bak", ".backup", ".orig", ".rej"))
        or bool(re.search(r"\.bak[-._][^/]+$", lowered))
    )


def discover_platform_builtin_skills(directory: Path, root: Path) -> list[Path]:
    """Record platform-owned Skill entries without scanning or admitting them."""
    found: list[Path] = []
    for current_raw, dirnames, filenames in os.walk(directory, followlinks=False):
        current = Path(current_raw)
        if not is_within(current, root):
            dirnames[:] = []
            continue
        dirnames[:] = [
            name
            for name in sorted(dirnames)
            if not is_link_or_reparse(current / name)
            and is_within(current / name, root)
        ]
        if "SKILL.md" in filenames:
            candidate = current / "SKILL.md"
            if not is_link_or_reparse(candidate) and is_within(candidate, root):
                found.append(candidate)
    return found


def walk_source(root: Path) -> dict[str, Any]:
    files: list[Path] = []
    symlinks: list[Path] = []
    escaped_paths: list[Path] = []
    excluded_dirs: list[Path] = []
    excluded_skill_entries: list[dict[str, str]] = []
    for current_raw, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(current_raw)
        if not is_within(current, root):
            escaped_paths.append(current)
            dirnames[:] = []
            continue
        kept_dirs: list[str] = []
        for dirname in sorted(dirnames):
            candidate = current / dirname
            if is_link_or_reparse(candidate):
                symlinks.append(candidate)
            elif not is_within(candidate, root):
                escaped_paths.append(candidate)
            elif dirname.lower() in EXCLUDED_DIR_NAMES:
                excluded_dirs.append(candidate)
                if (
                    current == root
                    and dirname.lower() in PLATFORM_BUILTIN_DIR_NAMES
                ):
                    excluded_skill_entries.extend(
                        {
                            "path": relative(skill, root),
                            "reason": "platform_builtin",
                        }
                        for skill in discover_platform_builtin_skills(candidate, root)
                    )
            else:
                kept_dirs.append(dirname)
        dirnames[:] = kept_dirs
        for filename in sorted(filenames):
            candidate = current / filename
            if is_link_or_reparse(candidate):
                symlinks.append(candidate)
            elif not is_within(candidate, root):
                escaped_paths.append(candidate)
            elif candidate.is_file():
                files.append(candidate)
    return {
        "files": files,
        "symlinks": symlinks,
        "escaped_paths": escaped_paths,
        "excluded_dirs": excluded_dirs,
        "excluded_skill_entries": sorted(
            excluded_skill_entries,
            key=lambda item: (item["reason"], item["path"]),
        ),
    }


def unique_issue(code: str, file_path: str, detail: Optional[str] = None) -> dict[str, str]:
    issue = {"code": code, "file": file_path}
    if detail:
        issue["detail"] = detail
    return issue


def scan_entry(
    source_label: str,
    root: Path,
    skill_file: Path,
    assigned_files: list[Path],
    assigned_symlinks: list[Path],
    assigned_escaped_paths: list[Path],
    assigned_excluded_dirs: list[Path],
    skill_dirs: set[Path],
    private_patterns: dict[str, re.Pattern[str]],
    available_license_files: list[Path],
) -> dict[str, Any]:
    skill_dir = skill_file.parent
    skill_text = skill_file.read_text(encoding="utf-8", errors="replace")
    name, frontmatter_license = parse_frontmatter(skill_text)
    blockers: list[dict[str, str]] = []
    reviews: list[dict[str, str]] = []
    commands: set[str] = set()
    env_vars: set[str] = set()
    side_effects: set[str] = set()
    license_files: list[str] = []
    scanned_files = 0
    total_bytes = 0
    content_hash = hashlib.sha256()

    if not name:
        blockers.append(unique_issue("missing_frontmatter_name", relative(skill_file, root)))
        name = skill_dir.name
    if name != skill_dir.name:
        blockers.append(
            unique_issue(
                "folder_name_mismatch",
                relative(skill_file, root),
                f"folder={skill_dir.name} frontmatter={name}",
            )
        )

    for path in sorted(assigned_files):
        rel = relative(path, root)
        local_rel = path.relative_to(skill_dir).as_posix()
        lower_name = path.name.lower()
        if is_backup_artifact(path.name):
            blockers.append(unique_issue("backup_or_recovery_artifact", rel))
        if lower_name in LICENSE_NAMES or lower_name.startswith(("license.", "notice.")):
            license_files.append(rel)
        try:
            size = path.stat().st_size
            raw = path.read_bytes()
        except OSError:
            blockers.append(unique_issue("unreadable_file", rel))
            continue
        total_bytes += size
        content_hash.update(local_rel.encode("utf-8"))
        content_hash.update(b"\0")
        content_hash.update(str(stat.S_IMODE(path.stat().st_mode) & 0o111).encode("ascii"))
        content_hash.update(b"\0")
        content_hash.update(raw)
        content_hash.update(b"\0")
        if size > MAX_TEXT_BYTES:
            blockers.append(
                unique_issue("oversized_file", rel, f"bytes={size}")
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if path.suffix.lower() in DANGEROUS_BINARY_EXTENSIONS:
                blockers.append(unique_issue("dangerous_binary_file", rel))
            else:
                detail = (
                    "known_asset_type"
                    if path.suffix.lower() in SAFE_BINARY_EXTENSIONS
                    else "unknown_binary_type"
                )
                reviews.append(unique_issue("binary_asset_review", rel, detail))
            continue
        except OSError:
            blockers.append(unique_issue("unreadable_file", rel))
            continue
        scanned_files += 1
        for label, pattern in private_patterns.items():
            if pattern.search(text):
                blockers.append(unique_issue(label, rel))
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                blockers.append(unique_issue(label, rel))
        for label, pattern in SENSITIVE_CANDIDATE_PATTERNS.items():
            if pattern.search(text) and not SECRET_PATTERNS[
                "openai_style_secret"
            ].search(text):
                reviews.append(unique_issue(label, rel))
        for command, pattern in COMMAND_PATTERNS.items():
            if pattern.search(text):
                commands.add(command)
        for pattern in ENV_PATTERNS:
            env_vars.update(pattern.findall(text))
        env_vars.difference_update(PROMPT_PLACEHOLDERS)
        for effect, pattern in SIDE_EFFECT_PATTERNS.items():
            if pattern.search(text):
                side_effects.add(effect)

    for path in sorted(assigned_symlinks):
        blockers.append(unique_issue("symlink", relative(path, root)))
    for path in sorted(assigned_escaped_paths):
        blockers.append(unique_issue("path_escape", relative(path, root)))
    for path in sorted(assigned_excluded_dirs):
        blockers.append(
            unique_issue(
                "excluded_artifact_directory",
                relative(path, root),
                f"name={path.name}",
            )
        )

    for path in sorted(available_license_files):
        if path.parent == root or path.parent == skill_dir or path.parent in skill_dir.parents:
            rel = relative(path, root)
            if rel not in license_files:
                license_files.append(rel)

    if not frontmatter_license and not license_files:
        reviews.append(unique_issue("missing_license_evidence", relative(skill_file, root)))
    if commands:
        reviews.append(
            unique_issue(
                "command_dependencies",
                relative(skill_file, root),
                ",".join(sorted(commands)),
            )
        )
    if env_vars:
        reviews.append(
            unique_issue(
                "environment_dependencies",
                relative(skill_file, root),
                ",".join(sorted(env_vars)),
            )
        )
    if side_effects:
        reviews.append(
            unique_issue(
                "side_effect_review",
                relative(skill_file, root),
                ",".join(sorted(side_effects)),
            )
        )

    ancestor = skill_dir.parent
    nested = False
    while ancestor != root and ancestor != ancestor.parent:
        if ancestor in skill_dirs:
            nested = True
            break
        ancestor = ancestor.parent

    if nested:
        reviews.append(
            unique_issue("nested_skill_entry", relative(skill_file, root))
        )

    issue_key = lambda issue: (
        issue["code"],
        issue["file"],
        issue.get("detail", ""),
    )
    blockers = [
        dict(items)
        for items in sorted(
            {tuple(sorted(issue.items())) for issue in blockers},
            key=lambda items: issue_key(dict(items)),
        )
    ]
    reviews = [
        dict(items)
        for items in sorted(
            {tuple(sorted(issue.items())) for issue in reviews},
            key=lambda items: issue_key(dict(items)),
        )
    ]
    technical_status = "blocked" if blockers else ("review" if reviews else "candidate")
    incomplete_codes = {
        "excluded_artifact_directory",
        "oversized_file",
        "path_escape",
        "symlink",
        "unreadable_file",
    }
    return {
        "name": name,
        "source": source_label,
        "path": relative(skill_file, root),
        "nested": nested,
        "files_scanned": scanned_files,
        "bytes": total_bytes,
        "content_sha256": content_hash.hexdigest(),
        "package_complete": not any(
            issue["code"] in incomplete_codes for issue in blockers
        ),
        "license": {
            "frontmatter": frontmatter_license,
            "files": sorted(license_files),
            "redistribution_status": "unreviewed",
        },
        "dependencies": {
            "commands": sorted(commands),
            "environment": sorted(env_vars),
        },
        "side_effects": sorted(side_effects),
        "blockers": blockers,
        "reviews": reviews,
        "technical_status": technical_status,
    }


def audit(
    sources: Iterable[tuple[str, Path]],
    private_terms: Iterable[str] = (),
    entry_mode: str = "recursive",
) -> dict[str, Any]:
    if entry_mode not in {"recursive", "top-level"}:
        raise ValueError(f"unsupported entry mode: {entry_mode}")
    sources = list(sources)
    source_priority = {
        label: index for index, (label, _) in enumerate(sources)
    }
    private_patterns = dict(PERSONAL_PATTERNS)
    for index, term in enumerate(private_terms, start=1):
        private_patterns[f"private_term_{index}"] = re.compile(
            re.escape(term), re.IGNORECASE
        )
    entries: list[dict[str, Any]] = []
    source_summaries: list[dict[str, Any]] = []
    for source_label, root in sources:
        walked = walk_source(root)
        files: list[Path] = walked["files"]
        skill_files = sorted(
            path
            for path in files
            if path.name == "SKILL.md"
            and (
                entry_mode == "recursive"
                or path.parent.parent == root
            )
        )
        skill_dirs = {path.parent for path in skill_files}
        available_license_files = [
            path
            for path in files
            if path.name.lower() in LICENSE_NAMES
            or path.name.lower().startswith(("license.", "notice."))
        ]
        files_by_skill: dict[Path, list[Path]] = defaultdict(list)
        symlinks_by_skill: dict[Path, list[Path]] = defaultdict(list)
        escaped_by_skill: dict[Path, list[Path]] = defaultdict(list)
        excluded_by_skill: dict[Path, list[Path]] = defaultdict(list)
        source_blockers: list[dict[str, str]] = []
        for path in files:
            owner = nearest_skill_dir(path, skill_dirs)
            if owner:
                files_by_skill[owner].append(path)
        for path in walked["symlinks"]:
            owner = nearest_skill_dir(path, skill_dirs)
            if owner:
                symlinks_by_skill[owner].append(path)
            else:
                source_blockers.append(
                    unique_issue("source_symlink", relative(path, root))
                )
        for path in walked["escaped_paths"]:
            owner = nearest_skill_dir(path, skill_dirs)
            if owner:
                escaped_by_skill[owner].append(path)
            else:
                source_blockers.append(
                    unique_issue("source_path_escape", relative(path, root))
                )
        for path in walked["excluded_dirs"]:
            if path.parent == root and path.name.lower() in PLATFORM_BUILTIN_DIR_NAMES:
                continue
            owner = nearest_skill_dir(path, skill_dirs)
            if owner:
                excluded_by_skill[owner].append(path)
            else:
                source_blockers.append(
                    unique_issue(
                        "source_excluded_artifact_directory",
                        relative(path, root),
                        f"name={path.name}",
                    )
                )
        source_entries = [
            scan_entry(
                source_label,
                root,
                skill_file,
                files_by_skill[skill_file.parent],
                symlinks_by_skill[skill_file.parent],
                escaped_by_skill[skill_file.parent],
                excluded_by_skill[skill_file.parent],
                skill_dirs,
                private_patterns,
                available_license_files,
            )
            for skill_file in skill_files
        ]
        entries.extend(source_entries)
        source_summaries.append(
            {
                "label": source_label,
                "entries": len(source_entries),
                "symlinks": len(walked["symlinks"]),
                "excluded_artifact_directories": len(walked["excluded_dirs"]),
                "excluded_skill_entries": walked["excluded_skill_entries"],
                "blockers": sorted(
                    source_blockers,
                    key=lambda issue: (
                        issue["code"],
                        issue["file"],
                        issue.get("detail", ""),
                    ),
                ),
            }
        )

    entries.sort(key=lambda item: (item["name"], item["source"], item["path"]))
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        by_name[entry["name"]].append(entry)
    duplicates = []
    for name, candidates in sorted(by_name.items()):
        if len(candidates) <= 1:
            continue
        identical_content = (
            len({item["content_sha256"] for item in candidates}) == 1
        )
        complete = all(item["package_complete"] for item in candidates)
        auto_deduplicate = identical_content and complete
        ranked = sorted(
            candidates,
            key=lambda item: (
                item["nested"],
                source_priority[item["source"]],
                item["path"],
            ),
        )
        duplicates.append({
            "name": name,
            "identical_content": identical_content,
            "complete_packages": complete,
            "resolution": (
                "auto_deduplicate" if auto_deduplicate else "manual_compare"
            ),
            "selection_policy": (
                "source_argument_order_then_non_nested"
                if auto_deduplicate
                else "manual_no_candidate"
            ),
            "canonical_candidate": (
                {"source": ranked[0]["source"], "path": ranked[0]["path"]}
                if auto_deduplicate
                else None
            ),
            "candidates": [
                {
                    "source": item["source"],
                    "path": item["path"],
                    "content_sha256": item["content_sha256"],
                }
                for item in candidates
            ],
        })
    duplicate_names = {item["name"] for item in duplicates}
    for entry in entries:
        if entry["name"] in duplicate_names:
            entry["blockers"].append(
                unique_issue("duplicate_name", entry["path"], entry["name"])
            )
            entry["blockers"].sort(
                key=lambda issue: (
                    issue["code"],
                    issue["file"],
                    issue.get("detail", ""),
                )
            )
            entry["technical_status"] = "blocked"

    statuses = Counter(entry["technical_status"] for entry in entries)
    blocker_codes = Counter(
        issue["code"] for entry in entries for issue in entry["blockers"]
    )
    for source in source_summaries:
        blocker_codes.update(issue["code"] for issue in source["blockers"])
    review_codes = Counter(
        issue["code"] for entry in entries for issue in entry["reviews"]
    )
    identical_duplicates = sum(
        1 for duplicate in duplicates if duplicate["identical_content"]
    )
    auto_deduplicable = sum(
        1 for duplicate in duplicates if duplicate["resolution"] == "auto_deduplicate"
    )
    return {
        "schema_version": 1,
        "sensitivity": "private_intake",
        "entry_mode": entry_mode,
        "sources": source_summaries,
        "summary": {
            "entries": len(entries),
            "unique_names": len(by_name),
            "duplicate_names": len(duplicates),
            "identical_duplicate_names": identical_duplicates,
            "conflicting_duplicate_names": len(duplicates) - identical_duplicates,
            "auto_deduplicable_names": auto_deduplicable,
            "manual_duplicate_names": len(duplicates) - auto_deduplicable,
            "source_blockers": sum(
                len(source["blockers"]) for source in source_summaries
            ),
            "technical_status": dict(sorted(statuses.items())),
            "blocker_codes": dict(sorted(blocker_codes.items())),
            "review_codes": dict(sorted(review_codes.items())),
        },
        "duplicates": duplicates,
        "entries": entries,
    }


def public_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": report["schema_version"],
        "sensitivity": "public_summary",
        "entry_mode": report["entry_mode"],
        "sources": [
            {
                "label": source["label"],
                "entries": source["entries"],
                "symlinks": source["symlinks"],
                "excluded_artifact_directories": source[
                    "excluded_artifact_directories"
                ],
                "excluded_skill_entries": len(source["excluded_skill_entries"]),
                "blockers": len(source["blockers"]),
            }
            for source in report["sources"]
        ],
        "summary": report["summary"],
    }


def write_report(
    report: dict[str, Any], output: Optional[Path], detailed: bool
) -> None:
    payload = report if detailed else public_summary(report)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output:
        output = output.expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.is_symlink():
            raise OSError(f"refusing to write report through symlink: {output}")
        descriptor, temp_name = tempfile.mkstemp(
            dir=str(output.parent),
            prefix=f".{output.name}.",
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(encoded)
            os.chmod(temp_name, 0o600)
            os.replace(temp_name, output)
        except BaseException:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise
    else:
        sys.stdout.write(encoded)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Skill source trees without copying their contents."
    )
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        type=parse_source,
        metavar="LABEL=PATH",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--report",
        choices=("summary", "detailed"),
        default="summary",
        help="detailed reports contain private intake metadata and require --output",
    )
    parser.add_argument(
        "--private-term",
        action="append",
        default=[],
        help="additional private name or workspace term to flag without recording its value",
    )
    parser.add_argument(
        "--entry-mode",
        choices=("recursive", "top-level"),
        default="recursive",
        help=(
            "recursive audits every discovered SKILL.md; top-level audits only "
            "runtime entries directly below each source root"
        ),
    )
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()
    labels = [label for label, _ in args.source]
    if len(labels) != len(set(labels)):
        parser.error("source labels must be unique")
    if any(not term.strip() for term in args.private_term):
        parser.error("private terms must not be empty")
    if args.report == "detailed" and not args.output:
        parser.error("detailed reports require --output")
    report = audit(args.source, args.private_term, args.entry_mode)
    write_report(report, args.output, args.report == "detailed")
    if args.fail_on_blockers and (
        report["summary"]["technical_status"].get("blocked")
        or report["summary"]["source_blockers"]
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
