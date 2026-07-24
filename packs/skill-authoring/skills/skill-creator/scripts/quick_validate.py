#!/usr/bin/env python3
"""
Quick validation script for skills
"""

import sys
import re
from pathlib import Path
import json

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def _parse_simple_yaml_frontmatter(frontmatter_text: str) -> dict:
    """
    Minimal YAML parser for simple key/value + nested dict via indentation.
    Supports the subset used in this workspace templates.
    """
    root: dict = {}
    stack = [(0, root)]  # (indent_level, obj)

    for raw_line in frontmatter_text.splitlines():
        if not raw_line.strip():
            continue
        stripped = raw_line.lstrip()
        if stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(stripped)
        key, sep, rest = stripped.partition(":")
        if not sep:
            continue

        # Adjust stack based on indentation
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()

        cur = stack[-1][1]
        value = rest.strip()
        if value == "":
            new_obj: dict = {}
            cur[key] = new_obj
            # Assume 2-space indent for nested blocks (good enough for templates)
            stack.append((indent + 2, new_obj))
            continue

        low = value.lower()
        if low == "true":
            parsed = True
        elif low == "false":
            parsed = False
        else:
            parsed = value.strip('"').strip("'")
        cur[key] = parsed

    return root


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        if yaml is None:
            frontmatter = _parse_simple_yaml_frontmatter(frontmatter_text)
        else:
            frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except Exception as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, f"Unexpected key(s): {', '.join(sorted(unexpected_keys))}"

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, "Frontmatter 'name' must be a string"
    name = name.strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' should be hyphen-case: lowercase letters, digits, hyphens"
    if name != skill_path.name:
        return False, f"Frontmatter name '{name}' must match directory name '{skill_path.name}'"

    description = frontmatter.get("description", "")
    if not isinstance(description, str) or not description.strip():
        return False, "Frontmatter 'description' must be a non-empty string"
    description = description.strip()
    if len(description) > 1024:
        return False, f"Frontmatter 'description' is too long ({len(description)} > 1024 characters)"

    # Optional: routing validation for newly created skills (opt-in via metadata)
    metadata = frontmatter.get("metadata") if isinstance(frontmatter, dict) else None
    routing_meta = None
    if isinstance(metadata, dict):
        routing_meta = metadata.get("routing")

    require_prompt = False
    require_file = False
    require_description_routing = False
    if isinstance(routing_meta, dict):
        require_prompt = bool(routing_meta.get("requirePromptTriggers"))
        require_file = bool(routing_meta.get("requireFileTriggers"))
        require_description_routing = bool(routing_meta.get("requireDescriptionRouting"))

    if require_prompt or require_file or require_description_routing:
        # Find routing file
        repo_root = None
        candidates = [skill_path.resolve()] + list(skill_path.resolve().parents)
        # Also try locating from this script's location (skill may live outside repo)
        script_path = Path(__file__).resolve()
        candidates.extend([script_path] + list(script_path.parents))

        for p in candidates:
            candidate = p / ".cursor" / "skill-rules.json"
            if candidate.exists():
                repo_root = p
                break

        if repo_root is None:
            return False, "Routing required but could not locate '.cursor/skill-rules.json'"

        routing_file = repo_root / ".cursor" / "skill-rules.json"
        try:
            data = json.loads(routing_file.read_text(encoding="utf-8"))
        except Exception as e:
            return False, f"Failed to read routing file: {routing_file} ({e})"

        skills = data.get("skills")
        if not isinstance(skills, dict):
            return False, f"Invalid routing file format (missing 'skills'): {routing_file}"

        entry = skills.get(name)
        if not isinstance(entry, dict):
            return False, f"Routing required but skill '{name}' not found in {routing_file}"

        prompt_triggers = entry.get("promptTriggers")
        file_triggers = entry.get("fileTriggers")

        if require_prompt:
            if not isinstance(prompt_triggers, dict):
                return False, f"Routing required: missing promptTriggers for '{name}'"
            keywords = prompt_triggers.get("keywords")
            intent_patterns = prompt_triggers.get("intentPatterns")
            if not isinstance(keywords, list) or len(keywords) == 0:
                return False, f"Routing required: promptTriggers.keywords must be a non-empty array for '{name}'"
            if not isinstance(intent_patterns, list) or len(intent_patterns) == 0:
                return False, f"Routing required: promptTriggers.intentPatterns must be a non-empty array for '{name}'"

        if require_file:
            if not isinstance(file_triggers, dict):
                return False, f"Routing required: missing fileTriggers for '{name}'"
            path_patterns = file_triggers.get("pathPatterns")
            if not isinstance(path_patterns, list) or len(path_patterns) == 0:
                return False, f"Routing required: fileTriggers.pathPatterns must be a non-empty array for '{name}'"

        if require_description_routing:
            # 1) Description should be "router-friendly" for preload
            if not 250 <= len(description) <= 450:
                return False, (
                    "Description routing required: description must be 250-450 characters "
                    f"(got {len(description)})"
                )
            if "TODO" in description or "[TBD" in description:
                return False, "Description routing required: description still contains TODO placeholder"
            if not re.search(r"(适用于|用于|Use when|use when)", description):
                return False, "Description routing required: description must contain a WHEN cue (e.g. '适用于…' / 'Use when …')"
            if not re.search(r"(即使.*(未|没有|不).*点名|未明确点名|Also trigger|also trigger)", description):
                return False, "Description routing required: missing implicit trigger cue for users who do not name the person"
            if not re.search(r"(分流|让位|优先)", description):
                return False, "Description routing required: missing adjacent-skill deconfliction cue"
            if not re.search(r"(不用于|不触发|Do not use|do not use)", description):
                return False, "Description routing required: missing negative trigger or safety boundary"
            if re.search(r"(基于.{0,24}(来源|调研)|一手占比|提炼\s*\d+\s*个核心|表达\s*DNA)", description, re.I):
                return False, "Description routing required: research provenance belongs in metadata/body, not description"

            # 2) Ensure description includes at least one keyword trigger (skip placeholders)
            keywords = None
            if isinstance(prompt_triggers, dict):
                keywords = prompt_triggers.get("keywords")
            keyword_hits = 0
            if isinstance(keywords, list):
                for kw in keywords:
                    if not isinstance(kw, str):
                        continue
                    s = kw.strip()
                    if not s or s.lower() == "todo":
                        continue
                    if s in description:
                        keyword_hits += 1
                        break
            if isinstance(keywords, list) and keyword_hits == 0:
                return False, "Description routing required: description must include at least one promptTriggers.keyword (for preload discovery)"

        resources = entry.get("resources")
        if not isinstance(resources, dict):
            return False, f"Routing required: missing resources for '{name}'"
        primary = resources.get("primary")
        expected_primary = f".cursor/skills/{name}/SKILL.md"
        if primary != expected_primary:
            return False, (
                f"Routing required: resources.primary mismatch for '{name}'. "
                f"Expected '{expected_primary}', got '{primary}'"
            )
        if not (repo_root / expected_primary).exists():
            return False, f"Routing required: resources.primary does not exist for '{name}'"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
