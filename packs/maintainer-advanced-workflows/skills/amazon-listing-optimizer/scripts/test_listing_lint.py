#!/usr/bin/env python3

from __future__ import annotations

import unittest
from datetime import date

from listing_lint import lint_bundle


def valid_bundle() -> dict:
    return {
        "scope": {
            "marketplace": "US",
            "locale": "en-US",
            "product_type": "ARTIFICIAL_PLANT",
            "mode": "BUILD",
            "child_asins": ["B0TEST001"],
        },
        "policy": {
            "checked_at": "2026-07-15",
            "effective_at": "2026-07-15",
            "source_url": "https://sellercentral.amazon.com/example",
            "title_max_chars": 75,
            "item_highlights_max_chars": 125,
            "item_highlights_supported": True,
            "max_age_days": 7,
        },
        "claims": [
            {
                "claim_id": "CL-001",
                "evidence_grade": "E2",
                "evidence_status": "verified_source",
                "evidence_source": "measurement.csv",
                "variants": ["B0TEST001"],
                "prohibited_wording": ["fits every planter"],
            },
            {
                "claim_id": "CL-002",
                "evidence_grade": "E1",
                "evidence_status": "verified_source",
                "evidence_source": "supplier-spec.pdf",
                "variants": ["B0TEST001"],
                "prohibited_wording": ["never fades"],
            },
        ],
        "listing": {
            "title": {"text": "Example Artificial Flowers, 12 Bundles, Outdoor Planters", "claim_ids": ["CL-001"]},
            "item_highlights": {"text": "Made with UV-treated material for porch and patio décor.", "claim_ids": ["CL-002"]},
            "bullets": [],
            "backend_terms": {"text": "faux greenery outdoor decor", "claim_ids": []},
        },
        "questions": [
            {
                "question_id": "Q-001",
                "priority": "P0",
                "status": "answered",
                "claim_ids": ["CL-002"],
                "field_refs": ["item_highlights"],
            }
        ],
        "competitor_brands": [],
        "forbidden_terms": ["best", "perfect", "never", "100%", "#1"],
        "approvals": {
            "product": {
                "status": "approved",
                "approver": "product-owner@company",
                "approved_at": "2026-07-15T09:00:00+08:00",
            },
            "compliance": {
                "status": "approved",
                "approver": "compliance-owner@company",
                "approved_at": "2026-07-15T09:05:00+08:00",
            },
            "operations": {
                "status": "approved",
                "approver": "ops-owner@company",
                "approved_at": "2026-07-15T09:10:00+08:00",
            },
        },
        "experiment": {
            "design": "observational",
            "objective": "component_learning",
            "changed_fields": ["title"],
            "confounders": ["price", "ads", "inventory"],
            "inference": "correlational",
            "mye_eligible": False,
        },
    }


class ListingLintTests(unittest.TestCase):
    def test_valid_review_bundle_passes_mechanical_gate(self) -> None:
        report = lint_bundle(valid_bundle(), mode="review", today=date(2026, 7, 15))
        self.assertEqual(report["summary"]["blockers"], 0)
        self.assertEqual(report["state"], "READY_FOR_HUMAN_REVIEW")
        self.assertTrue(report["summary"]["not_a_compliance_verdict"])

    def test_draft_without_approvals_warns_but_does_not_block(self) -> None:
        bundle = valid_bundle()
        bundle["approvals"] = {}
        report = lint_bundle(bundle, mode="draft", today=date(2026, 7, 15))
        self.assertEqual(report["summary"]["blockers"], 0)
        self.assertGreaterEqual(report["summary"]["warnings"], 1)
        self.assertEqual(report["state"], "DRAFT_UNVERIFIED")

    def test_overclaim_and_false_causality_block(self) -> None:
        bundle = valid_bundle()
        bundle["claims"][1]["evidence_grade"] = "E0"
        bundle["listing"]["title"]["text"] = "Best " + ("X" * 90)
        bundle["listing"]["item_highlights"]["text"] = "Never fades, 100% perfect."
        bundle["experiment"] = {
            "design": "observational",
            "objective": "component_learning",
            "changed_fields": ["title", "main_image", "price"],
            "inference": "randomized",
            "confounders": [],
        }
        bundle["approvals"] = {}
        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))
        check_ids = {item["check_id"] for item in report["checks"] if item["verdict"] == "BLOCK"}
        self.assertGreater(report["summary"]["blockers"], 4)
        self.assertTrue({"L-01", "L-03", "L-04", "L-07", "L-08"}.issubset(check_ids))
        self.assertEqual(report["state"], "BLOCKED_RISK")

    def test_stale_policy_blocks_review_but_only_warns_in_draft(self) -> None:
        bundle = valid_bundle()
        bundle["policy"]["checked_at"] = "2026-07-01"
        review = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))
        draft = lint_bundle(bundle, mode="draft", today=date(2026, 7, 15))

        self.assertEqual(review["state"], "BLOCKED_RISK")
        self.assertTrue(
            any(
                item["check_id"] == "L-01" and item["verdict"] == "BLOCK"
                for item in review["checks"]
            )
        )
        self.assertEqual(draft["state"], "DRAFT_UNVERIFIED")
        self.assertTrue(
            any(
                item["check_id"] == "L-01" and item["verdict"] == "WARN"
                for item in draft["checks"]
            )
        )

    def test_claim_must_cover_the_bundle_target_child_asin(self) -> None:
        bundle = valid_bundle()
        bundle["scope"]["child_asins"] = ["B0WHITE01"]

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "BLOCKED_RISK")
        self.assertTrue(
            any(
                item["check_id"] == "L-02"
                and item["verdict"] == "BLOCK"
                and "target child ASIN B0WHITE01" in item["message"]
                for item in report["checks"]
            )
        )

    def test_multi_child_migration_requires_one_lint_bundle_per_child(self) -> None:
        bundle = valid_bundle()
        bundle["scope"]["child_asins"] = ["B0RED0001", "B0WHITE01"]

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "BLOCKED_RISK")
        self.assertTrue(
            any(
                item["check_id"] == "L-02"
                and "one child ASIN per bundle" in item["message"]
                for item in report["checks"]
            )
        )

    def test_pending_strings_cannot_masquerade_as_human_approvals(self) -> None:
        bundle = valid_bundle()
        bundle["approvals"] = {
            "product": "pending",
            "compliance": "pending",
            "operations": "pending",
        }

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "BLOCKED_RISK")
        self.assertTrue(
            any(item["check_id"] == "L-07" and item["verdict"] == "BLOCK" for item in report["checks"])
        )

    def test_answered_p0_question_requires_real_claim_and_matching_field(self) -> None:
        bundle = valid_bundle()
        bundle["questions"][0]["claim_ids"] = ["UNKNOWN"]
        bundle["questions"][0]["field_refs"] = ["bullet_99"]

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "BLOCKED_RISK")
        coverage = next(item for item in report["checks"] if item["check_id"] == "L-06")
        statuses = {item["status"] for item in coverage["evidence"]["uncovered"]}
        self.assertTrue({"unknown_claim", "unknown_or_hidden_field"}.issubset(statuses))

    def test_future_or_unsupported_policy_cannot_pass_review(self) -> None:
        bundle = valid_bundle()
        bundle["policy"]["effective_at"] = "2026-07-27"
        bundle["policy"]["item_highlights_supported"] = False

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "BLOCKED_RISK")
        policy_blocks = [
            item for item in report["checks"] if item["check_id"] == "L-01" and item["verdict"] == "BLOCK"
        ]
        self.assertGreaterEqual(len(policy_blocks), 2)

    def test_missing_scope_returns_needs_input(self) -> None:
        bundle = valid_bundle()
        bundle["scope"].pop("product_type")

        report = lint_bundle(bundle, mode="review", today=date(2026, 7, 15))

        self.assertEqual(report["state"], "NEEDS_INPUT")


if __name__ == "__main__":
    unittest.main()
