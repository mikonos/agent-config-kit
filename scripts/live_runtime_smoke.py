#!/usr/bin/env python3
"""Generate and check the read-only live Runtime Skill-routing smoke test."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "catalog" / "live_runtime_smoke.json"


class SmokeError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SmokeError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SmokeError(f"expected JSON object: {path}")
    return value


def normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def validate_contract(root: Path, contract: dict[str, Any]) -> list[dict[str, Any]]:
    manifest = load_object(root / "manifest.json")
    packs = manifest.get("skill_packs")
    if manifest.get("schema_version") != 1 or not isinstance(packs, dict):
        raise SmokeError("invalid package manifest")
    skill_packs: dict[str, str] = {}
    for pack_name, names in packs.items():
        if not isinstance(pack_name, str) or not isinstance(names, list):
            raise SmokeError("invalid Skill pack")
        for name in names:
            if not isinstance(name, str) or name in skill_packs:
                raise SmokeError(f"invalid or duplicate packaged Skill: {name}")
            skill_packs[name] = pack_name

    constraints = contract.get("constraints")
    cases = contract.get("cases")
    if (
        contract.get("schema_version") != 1
        or constraints
        != {
            "file_writes": False,
            "network_beyond_model_call": False,
            "session_persistence": False,
            "tools": "read_only_skill_inspection",
        }
        or not isinstance(cases, list)
        or not cases
    ):
        raise SmokeError("invalid live Runtime smoke contract")

    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {
            "expected_skill",
            "id",
            "scenario_zh",
            "source_anchors",
        }:
            raise SmokeError("invalid live Runtime smoke case")
        case_id = case.get("id")
        skill = case.get("expected_skill")
        scenario = case.get("scenario_zh")
        anchors = case.get("source_anchors")
        if (
            not isinstance(case_id, str)
            or not case_id
            or case_id in seen
            or not isinstance(skill, str)
            or not skill
            or not isinstance(scenario, str)
            or not scenario.strip()
            or not isinstance(anchors, list)
            or len(anchors) < 2
            or any(not isinstance(item, str) or not item.strip() for item in anchors)
        ):
            raise SmokeError("invalid live Runtime smoke case")
        seen.add(case_id)
        pack_name = skill_packs.get(skill)
        if pack_name is None:
            raise SmokeError(f"smoke Skill is not packaged: {skill}")
        skill_path = root / "packs" / pack_name / "skills" / skill / "SKILL.md"
        if not skill_path.is_file():
            raise SmokeError(f"smoke Skill is missing: {skill}")
        text = skill_path.read_text(encoding="utf-8")
        end = text.find("\n---", 4)
        if end < 0:
            raise SmokeError(f"smoke Skill frontmatter is invalid: {skill}")
        skill_body = normalize(text[end + 4 :])
        for phrase in anchors:
            if normalize(phrase) not in skill_body:
                raise SmokeError(
                    f"smoke evidence no longer matches {skill}: {phrase}"
                )
        case["_normalized_skill_body"] = skill_body
    return cases


def render_prompt(cases: list[dict[str, Any]]) -> str:
    scenarios = "\n".join(
        f"- {case['id']}：{case['scenario_zh']}" for case in cases
    )
    return f"""不要联网、不要修改文件。
仅可使用 Runtime 的只读 Skill、只读文件能力或只读命令读取
all-skills-router、它的本地索引和候选 Skill 的 SKILL.md；
不要调用 MCP、浏览器、连接器或其他工具。
只根据当前项目已经加载的 Rule 和 Skill 完成一次路由检查。

对每个场景：
1. 选择一个最匹配的已加载 Skill；
2. 从该 Skill 正文逐字复制两段能证明其方法匹配的短英文原文；
3. 不要解释，只返回严格 JSON，不要使用 Markdown 代码围栏。

场景：
{scenarios}

返回格式：
{{"results":[{{"id":"场景 id","skill":"Skill 名称","evidence":["英文原文一","英文原文二"]}}]}}
"""


def validate_response(
    cases: list[dict[str, Any]], response: dict[str, Any]
) -> None:
    if set(response) != {"results"} or not isinstance(response["results"], list):
        raise SmokeError("response must contain only a results array")
    results = response["results"]
    if len(results) != len(cases):
        raise SmokeError("response does not contain every smoke case")
    by_id: dict[str, dict[str, Any]] = {}
    for result in results:
        if (
            not isinstance(result, dict)
            or set(result) != {"evidence", "id", "skill"}
            or not isinstance(result.get("id"), str)
            or result["id"] in by_id
            or not isinstance(result.get("skill"), str)
            or not isinstance(result.get("evidence"), list)
            or len(result["evidence"]) != 2
            or any(not isinstance(item, str) for item in result["evidence"])
        ):
            raise SmokeError("invalid result entry")
        by_id[result["id"]] = result
    for case in cases:
        case_id = case["id"]
        result = by_id.get(case_id)
        if result is None:
            raise SmokeError(f"missing smoke case: {case_id}")
        if result["skill"] != case["expected_skill"]:
            raise SmokeError(
                f"{case_id}: expected {case['expected_skill']}, "
                f"got {result['skill']}"
            )
        normalized_evidence = [normalize(item) for item in result["evidence"]]
        if (
            len(set(normalized_evidence)) != 2
            or any(len(item) < 8 for item in normalized_evidence)
        ):
            raise SmokeError(f"{case_id}: method evidence must be two distinct excerpts")
        skill_body = case["_normalized_skill_body"]
        for excerpt in normalized_evidence:
            if excerpt not in skill_body:
                raise SmokeError(
                    f"{case_id}: method evidence is not in the selected Skill body"
                )


def read_response(path_value: str) -> dict[str, Any]:
    if path_value == "-":
        try:
            value = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            raise SmokeError(f"invalid response JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise SmokeError("response must be a JSON object")
        return value
    return load_object(Path(path_value))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-contract")
    subparsers.add_parser("prompt")
    check = subparsers.add_parser("check-response")
    check.add_argument("response", help="response JSON path, or - for stdin")
    args = parser.parse_args()

    try:
        contract = load_object(CONTRACT_PATH)
        cases = validate_contract(ROOT, contract)
        if args.command == "prompt":
            print(render_prompt(cases), end="")
        elif args.command == "check-response":
            validate_response(cases, read_response(args.response))
            print(
                "LIVE RUNTIME RESPONSE PASS: "
                f"routing={len(cases)} "
                f"method_evidence={sum(len(case['source_anchors']) for case in cases)}"
            )
        else:
            print(
                "LIVE RUNTIME CONTRACT OK: "
                f"routing={len(cases)} "
                f"method_evidence={sum(len(case['source_anchors']) for case in cases)}"
            )
    except SmokeError as exc:
        print(f"LIVE RUNTIME SMOKE FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
