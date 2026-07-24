#!/usr/bin/env python3
"""Deterministic mechanical lint for Amazon Listing candidate bundles.

Exit codes:
  0: no blockers
  2: one or more blockers
  3: invalid input/schema or I/O error

This script does not decide whether evidence is true, a claim is lawful, or copy is
commercially persuasive. It only checks the supplied policy/evidence contract.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


VALID_GRADES = {"E0", "E1", "E2", "E3"}
VALID_EVIDENCE_STATUS = {
    "verified_source",
    "needs_verification",
    "conflicting",
    "expired",
}
VALID_INFERENCE = {"randomized", "correlational", "observational", "inconclusive"}
RANDOMIZED_DESIGNS = {"MYE_randomized", "randomized"}
DEFAULT_RISK_TERMS = ["best", "perfect", "never", "100%", "#1"]


class InputError(ValueError):
    """Raised for malformed bundles that cannot be meaningfully linted."""


def _as_dict(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{path} must be an object")
    return value


def _as_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise InputError(f"{path} must be an array")
    return value


def _iso_date(value: Any, path: str) -> date:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{path} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InputError(f"{path} must use YYYY-MM-DD") from exc


def _approval_issues(value: Any) -> list[str]:
    """Return reasons an approval record is not a traceable human approval."""
    if not isinstance(value, dict):
        return ["must be an object"]

    issues: list[str] = []
    if value.get("status") != "approved":
        issues.append("status must be approved")
    approver = value.get("approver")
    if not isinstance(approver, str) or not approver.strip():
        issues.append("approver is required")

    approved_at = value.get("approved_at")
    if not isinstance(approved_at, str) or not approved_at.strip():
        issues.append("approved_at is required")
    else:
        try:
            parsed = datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                issues.append("approved_at must include a timezone")
        except ValueError:
            issues.append("approved_at must be ISO-8601")
    return issues


def _norm(text: str) -> str:
    return " ".join(text.casefold().split())


def _contains(text: str, needle: str) -> bool:
    return _norm(needle) in _norm(text)


def _field_rows(listing: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("title", "item_highlights", "backend_terms"):
        value = listing.get(key)
        if value is None:
            continue
        item = _as_dict(value, f"listing.{key}")
        rows.append(
            {
                "field_id": key,
                "text": item.get("text", ""),
                "claim_ids": item.get("claim_ids", []),
                "visible": key != "backend_terms",
            }
        )

    for index, value in enumerate(listing.get("bullets", []), start=1):
        item = _as_dict(value, f"listing.bullets[{index - 1}]")
        rows.append(
            {
                "field_id": item.get("field_id") or f"bullet_{index}",
                "text": item.get("text", ""),
                "claim_ids": item.get("claim_ids", []),
                "visible": True,
            }
        )
    return rows


def lint_bundle(bundle: dict[str, Any], *, mode: str, today: date) -> dict[str, Any]:
    if mode not in {"draft", "review"}:
        raise InputError("mode must be draft or review")

    scope = _as_dict(bundle.get("scope"), "scope")
    policy = _as_dict(bundle.get("policy"), "policy")
    listing = _as_dict(bundle.get("listing"), "listing")
    claims_raw = _as_list(bundle.get("claims"), "claims")
    questions = _as_list(bundle.get("questions", []), "questions")
    approvals = _as_dict(bundle.get("approvals", {}), "approvals")
    experiment = _as_dict(bundle.get("experiment", {}), "experiment")

    checks: list[dict[str, Any]] = []

    def add(check_id: str, verdict: str, message: str, evidence: Any = None) -> None:
        checks.append(
            {
                "check_id": check_id,
                "verdict": verdict,
                "message": message,
                "evidence": evidence,
            }
        )

    # L-01: scope, policy freshness, supplied limits, and actual field lengths.
    missing_scope = [
        key
        for key in ("marketplace", "locale", "product_type", "mode")
        if not scope.get(key)
    ]
    if missing_scope:
        add("L-01", "BLOCK", "Missing scope fields", missing_scope)

    source_url = policy.get("source_url")
    checked_at_raw = policy.get("checked_at")
    if not source_url:
        add("L-01", "BLOCK" if mode == "review" else "WARN", "Policy source URL is missing")
    if not checked_at_raw:
        add("L-01", "BLOCK" if mode == "review" else "WARN", "policy.checked_at is missing")
        checked_at = None
    else:
        checked_at = _iso_date(checked_at_raw, "policy.checked_at")

    max_age_days = policy.get("max_age_days", 7)
    if not isinstance(max_age_days, int) or max_age_days < 0:
        raise InputError("policy.max_age_days must be a non-negative integer")
    if checked_at is not None:
        age_days = (today - checked_at).days
        verdict = "PASS"
        if age_days < 0:
            verdict = "BLOCK"
        elif age_days > max_age_days:
            verdict = "BLOCK" if mode == "review" else "WARN"
        add(
            "L-01",
            verdict,
            "Policy freshness measured against the supplied threshold",
            {"checked_at": str(checked_at), "today": str(today), "age_days": age_days, "max_age_days": max_age_days},
        )

    decision_date = today
    target_date_raw = scope.get("target_date")
    if target_date_raw:
        decision_date = _iso_date(target_date_raw, "scope.target_date")

    effective_at_raw = policy.get("effective_at")
    if not effective_at_raw:
        add("L-01", "BLOCK" if mode == "review" else "WARN", "policy.effective_at is missing")
    else:
        effective_at = _iso_date(effective_at_raw, "policy.effective_at")
        add(
            "L-01",
            "PASS" if effective_at <= decision_date else ("BLOCK" if mode == "review" else "WARN"),
            "Policy effective date applies to the review target date",
            {"effective_at": str(effective_at), "decision_date": str(decision_date)},
        )

    item_highlights = listing.get("item_highlights")
    if item_highlights is not None:
        item_highlights_text = _as_dict(item_highlights, "listing.item_highlights").get("text", "")
        if item_highlights_text and policy.get("item_highlights_supported") is not True:
            add(
                "L-01",
                "BLOCK" if mode == "review" else "WARN",
                "Item Highlights candidate requires item_highlights_supported=true",
                {"item_highlights_supported": policy.get("item_highlights_supported")},
            )

    limits = {
        "title": policy.get("title_max_chars"),
        "item_highlights": policy.get("item_highlights_max_chars"),
    }
    for field_id, limit in limits.items():
        field = listing.get(field_id)
        if field is None:
            continue
        if not isinstance(limit, int) or limit <= 0:
            add("L-01", "BLOCK" if mode == "review" else "WARN", f"Missing valid live limit for {field_id}")
            continue
        item = _as_dict(field, f"listing.{field_id}")
        text = item.get("text", "")
        if not isinstance(text, str):
            raise InputError(f"listing.{field_id}.text must be a string")
        measured = len(text)
        add(
            "L-01",
            "PASS" if measured <= limit else "BLOCK",
            f"{field_id} character count",
            {"measured": measured, "limit": limit, "counting": "Python Unicode code points; platform receipt remains authoritative"},
        )

    # L-02/L-03: claim identity, evidence, and variant scope.
    claim_ids = [item.get("claim_id") for item in claims_raw if isinstance(item, dict)]
    duplicates = sorted(k for k, v in Counter(claim_ids).items() if k and v > 1)
    if duplicates:
        add("L-02", "BLOCK", "Duplicate claim IDs", duplicates)

    claims: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(claims_raw):
        claim = _as_dict(raw, f"claims[{index}]")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id:
            add("L-02", "BLOCK", "Claim is missing claim_id", {"index": index})
            continue
        claims[claim_id] = claim
        grade = claim.get("evidence_grade")
        status = claim.get("evidence_status")
        if grade not in VALID_GRADES:
            add("L-03", "BLOCK", f"Invalid evidence grade for {claim_id}", grade)
        if status not in VALID_EVIDENCE_STATUS:
            add("L-03", "BLOCK", f"Invalid evidence status for {claim_id}", status)
        if grade == "E0" or status != "verified_source" or not claim.get("evidence_source"):
            add(
                "L-03",
                "BLOCK",
                f"Claim {claim_id} is not publishable evidence",
                {"grade": grade, "status": status, "source": claim.get("evidence_source")},
            )

    target_variants_raw = _as_list(scope.get("child_asins", []), "scope.child_asins")
    if len(target_variants_raw) > 1:
        add(
            "L-02",
            "BLOCK",
            "Lint one child ASIN per bundle; run separate bundles for a multi-child migration",
            target_variants_raw,
        )
    target_variant = target_variants_raw[0] if len(target_variants_raw) == 1 else None
    field_rows = _field_rows(listing)
    field_claim_refs: dict[str, set[str]] = defaultdict(set)
    all_text = "\n".join(str(row["text"]) for row in field_rows)

    for row in field_rows:
        if not isinstance(row["text"], str):
            raise InputError(f"{row['field_id']}.text must be a string")
        refs = _as_list(row["claim_ids"], f"{row['field_id']}.claim_ids")
        if row["visible"] and row["text"].strip() and not refs:
            add("L-02", "BLOCK", f"Visible field {row['field_id']} has text but no claim IDs")
        for claim_id in refs:
            if claim_id not in claims:
                add("L-02", "BLOCK", f"Unknown claim ID {claim_id} in {row['field_id']}")
                continue
            field_claim_refs[claim_id].add(row["field_id"])
            variants = set(claims[claim_id].get("variants") or [])
            if target_variant and target_variant not in variants:
                add(
                    "L-02",
                    "BLOCK",
                    f"Claim {claim_id} does not cover target child ASIN {target_variant}",
                    {"target_variant": target_variant, "claim_variants": sorted(variants)},
                )

    # L-04: local risk terms, competitors, and claim-specific prohibited wording.
    terms = bundle.get("forbidden_terms", DEFAULT_RISK_TERMS)
    terms = _as_list(terms, "forbidden_terms")
    term_hits = sorted({term for term in terms if isinstance(term, str) and term and _contains(all_text, term)})
    if term_hits:
        add("L-04", "BLOCK", "Forbidden/risk terms found", term_hits)

    competitors = _as_list(bundle.get("competitor_brands", []), "competitor_brands")
    competitor_hits = sorted({brand for brand in competitors if isinstance(brand, str) and brand and _contains(all_text, brand)})
    if competitor_hits:
        add("L-04", "BLOCK", "Competitor brands found in candidate content", competitor_hits)

    for claim_id, claim in claims.items():
        prohibited = claim.get("prohibited_wording", [])
        prohibited = _as_list(prohibited, f"claims[{claim_id}].prohibited_wording")
        hits = sorted({term for term in prohibited if isinstance(term, str) and term and _contains(all_text, term)})
        if hits:
            add("L-04", "BLOCK", f"Prohibited wording found for {claim_id}", hits)
        if claim.get("evidence_grade") == "E1":
            e1_hits = sorted({term for term in DEFAULT_RISK_TERMS if _contains(all_text, term)})
            if e1_hits:
                add("L-03", "BLOCK", f"E1 claim {claim_id} appears with absolute wording", e1_hits)

    # L-05: duplicated claim responsibility is a warning, not an Amazon policy claim.
    repeated = {claim_id: sorted(fields) for claim_id, fields in field_claim_refs.items() if len(fields) >= 3}
    if repeated:
        add("L-05", "WARN", "Claims repeated across three or more fields; review field responsibility", repeated)
    else:
        add("L-05", "PASS", "No claim is mechanically repeated across three or more fields")

    # L-06: priority questions must be answered by publishable claims in real visible fields.
    uncovered: list[dict[str, Any]] = []
    visible_fields = {row["field_id"]: row for row in field_rows if row["visible"]}
    for index, raw in enumerate(questions):
        question = _as_dict(raw, f"questions[{index}]")
        if question.get("priority") != "P0":
            continue
        status = question.get("status")
        if status not in {"answered", "explicit_gap", "product_issue"}:
            uncovered.append({"question_id": question.get("question_id"), "status": status})
        if status != "answered":
            continue

        question_id = question.get("question_id")
        question_claim_ids = _as_list(question.get("claim_ids", []), f"questions[{index}].claim_ids")
        field_refs = _as_list(question.get("field_refs", []), f"questions[{index}].field_refs")
        if not question_claim_ids:
            uncovered.append({"question_id": question_id, "status": "answered_without_claim_id"})
        if not field_refs:
            uncovered.append({"question_id": question_id, "status": "answered_without_field_ref"})

        valid_question_claim_ids: set[str] = set()
        for claim_id in question_claim_ids:
            claim = claims.get(claim_id)
            if claim is None:
                uncovered.append({"question_id": question_id, "status": "unknown_claim", "claim_id": claim_id})
                continue
            if (
                claim.get("evidence_grade") == "E0"
                or claim.get("evidence_status") != "verified_source"
                or not claim.get("evidence_source")
            ):
                uncovered.append({"question_id": question_id, "status": "unpublishable_claim", "claim_id": claim_id})
                continue
            valid_question_claim_ids.add(claim_id)

        for field_ref in field_refs:
            field = visible_fields.get(field_ref)
            if field is None:
                uncovered.append({"question_id": question_id, "status": "unknown_or_hidden_field", "field_ref": field_ref})
                continue
            field_claim_ids = set(_as_list(field["claim_ids"], f"listing.{field_ref}.claim_ids"))
            if valid_question_claim_ids and not valid_question_claim_ids.intersection(field_claim_ids):
                uncovered.append(
                    {
                        "question_id": question_id,
                        "status": "field_does_not_reference_question_claim",
                        "field_ref": field_ref,
                        "question_claim_ids": sorted(valid_question_claim_ids),
                    }
                )
    add("L-06", "PASS" if not uncovered else "BLOCK", "Priority question coverage", {"uncovered": uncovered})

    # L-07: the model must not manufacture approvals. Review mode requires traceable human approvals.
    invalid_approvals = {
        role: _approval_issues(approvals.get(role))
        for role in ("product", "compliance", "operations")
    }
    invalid_approvals = {role: issues for role, issues in invalid_approvals.items() if issues}
    if invalid_approvals:
        add(
            "L-07",
            "BLOCK" if mode == "review" else "WARN",
            "Human approvals are incomplete",
            invalid_approvals,
        )
    else:
        add("L-07", "PASS", "Traceable human approvals supplied", approvals)

    # L-08: prevent causal stories from observational or multi-change data.
    design = experiment.get("design", "none")
    inference = experiment.get("inference", "inconclusive")
    if inference not in VALID_INFERENCE:
        add("L-08", "BLOCK", "Invalid inference label", inference)
    if inference == "randomized" and design not in RANDOMIZED_DESIGNS:
        add("L-08", "BLOCK", "Randomized inference requires a randomized design", {"design": design})
    if design == "MYE_randomized" and experiment.get("mye_eligible") is not True:
        add("L-08", "BLOCK", "MYE design declared without verified eligibility")

    changed_fields = experiment.get("changed_fields", [])
    changed_fields = _as_list(changed_fields, "experiment.changed_fields")
    objective = experiment.get("objective", "monitoring")
    if len(changed_fields) > 1 and objective == "component_learning":
        add(
            "L-08",
            "BLOCK",
            "Component attribution cannot use several changed fields",
            changed_fields,
        )
    elif len(changed_fields) > 1:
        add("L-08", "WARN", "Multi-attribute run can compare packages, not component contribution", changed_fields)
    if design == "observational" and not experiment.get("confounders"):
        add("L-08", "WARN", "Observational design has no confounder log")

    blockers = [check for check in checks if check["verdict"] == "BLOCK"]
    warnings = [check for check in checks if check["verdict"] == "WARN"]
    if missing_scope:
        state = "NEEDS_INPUT"
    elif blockers:
        state = "BLOCKED_RISK"
    elif mode == "review":
        state = "READY_FOR_HUMAN_REVIEW"
    else:
        state = "DRAFT_UNVERIFIED"

    return {
        "schema_version": "1.1",
        "mode": mode,
        "state": state,
        "summary": {
            "blockers": len(blockers),
            "warnings": len(warnings),
            "checks": len(checks),
            "mechanical_pass": len(blockers) == 0,
            "not_a_compliance_verdict": True,
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint an evidence-backed Amazon Listing bundle")
    parser.add_argument("bundle", help="Path to the normalized JSON bundle")
    parser.add_argument("--mode", choices=["draft", "review"], default="draft")
    parser.add_argument("--today", help="Override current date for reproducible tests (YYYY-MM-DD)")
    parser.add_argument("--out", help="Write JSON report to this path; stdout is always emitted")
    args = parser.parse_args()

    try:
        bundle_path = Path(args.bundle)
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        if not isinstance(bundle, dict):
            raise InputError("bundle root must be an object")
        current_day = _iso_date(args.today, "--today") if args.today else date.today()
        report = lint_bundle(bundle, mode=args.mode, today=current_day)
        rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(rendered, encoding="utf-8")
        sys.stdout.write(rendered)
        return 2 if report["summary"]["blockers"] else 0
    except (OSError, json.JSONDecodeError, InputError) as exc:
        sys.stderr.write(f"INPUT_ERROR: {exc}\n")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
