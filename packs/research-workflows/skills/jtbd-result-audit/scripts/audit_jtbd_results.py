#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


KEY_FIELDS = [
    "purchase_type_normalized",
    "support_level_for_family_ai_brain_normalized",
    "unmet_need_normalized",
    "hire_job_normalized",
    "satisfaction_point_normalized",
    "dissatisfaction_point_normalized",
]

RISK_BUCKET_NAMES = [
    "high_risk_missing_coder_note",
    "screen_only_with_strong_family_signal",
    "screen_only_family_gift_context",
    "screen_only_family_operational_signal",
    "screen_only_family_mixed_or_other",
    "coordination_layer_short_weak_evidence",
    "supports_core_short_weak_evidence",
    "tool_pain_short_generic_positive",
    "purchase_unclear_short",
    "unmet_unclear_all",
]

HIGH_RISK_LABELS = {
    "purchase_type_normalized": {"unclear"},
    "support_level_for_family_ai_brain_normalized": {"screen_only"},
    "unmet_need_normalized": {"unclear"},
}

FAMILY_STRONG_RE = re.compile(
    r"\b("
    r"family|families|kids?|children|parents?|mom|moms|dad|dads|"
    r"wife|husband|spouse|partner|everyone|shared|same page|"
    r"our family|whole family|busy family|busy mom|caregiver|babysitter|"
    r"chores?|household|our routine|manage our family schedule"
    r")\b",
    re.I,
)

FAMILY_WEAK_RE = re.compile(
    r"\b(organized|organization|organizing|helpful|easy to use|efficient|routine)\b",
    re.I,
)

GIFT_CONTEXT_RE = re.compile(
    r"\b(gift|mother.?s day|birthday|mom|my mom|wife loved|wife loves|my wife|husband|family gift)\b",
    re.I,
)

OPERATIONAL_FAMILY_RE = re.compile(
    r"\b(family schedule|kids?|children|chores|shared|same page|calendar|sync|organized|household|manage)\b",
    re.I,
)

CONCRETE_TOOL_RE = re.compile(
    r"\b("
    r"calendar|schedule|sync|google|outlook|wifi|connect|subscription|"
    r"scan|flyers?|photos?|photo|frame|app|setup|install|upload|"
    r"remember|organized|organization|manage|management|routine|"
    r"useful|helpful|convenient|easy|works?|investment|planner|"
    r"kids?|family|wife|husband|partner|parents?"
    r")\b",
    re.I,
)

GENERIC_POSITIVE_RE = re.compile(
    r"\b("
    r"great|good|awesome|amazing|love|perfect|fantastic|excellent|"
    r"user friendly|easy|convenient|works?|helpful|must have|nice"
    r")\b",
    re.I,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Systematically audit JTBD review result JSON batches.")
    parser.add_argument("--review-csv", required=True, help="Path to clean_reviews.csv")
    parser.add_argument(
        "--batch",
        action="append",
        required=True,
        help="Batch definition in the form name=/path/to/final_out",
    )
    parser.add_argument("--audit-dir", required=True, help="Directory for summary/report/risk CSV outputs")
    parser.add_argument("--report-title", default="", help="Optional markdown report title")
    return parser.parse_args()


def parse_batches(batch_args: list[str]) -> dict[str, Path]:
    batches: dict[str, Path] = {}
    for item in batch_args:
        if "=" not in item:
            raise SystemExit(f"Invalid --batch value: {item}. Expected name=/path/to/out")
        name, raw_path = item.split("=", 1)
        name = name.strip()
        batch_path = Path(raw_path.strip())
        if not name or not batch_path.exists():
            raise SystemExit(f"Invalid batch definition: {item}")
        batches[name] = batch_path
    return batches


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_reviews(review_csv: Path) -> dict[str, dict[str, str]]:
    reviews = {}
    with review_csv.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            reviews[row["review_id"]] = row
    return reviews


def normalize_text(row: dict[str, str]) -> str:
    return f"{row.get('title_raw', '')} {row.get('content_raw', '')}".strip().replace("\n", " ")


def load_outputs(batches: dict[str, Path]) -> list[dict]:
    records: list[dict] = []
    for batch_name, base in batches.items():
        for path in sorted(base.glob("*.json")):
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
            data["_batch"] = batch_name
            data["_path"] = str(path)
            records.append(data)
    return records


def compute_distribution(records: list[dict], field: str) -> dict:
    counter = Counter()
    missing = 0
    for rec in records:
        value = rec.get(field)
        if value in (None, ""):
            missing += 1
        else:
            counter[str(value)] += 1
    return {
        "missing": missing,
        "counts": dict(counter.most_common()),
        "total_non_missing": sum(counter.values()),
    }


def top_pct(count: int, total: int) -> float:
    return round(count * 100.0 / total, 2) if total else 0.0


def summarize_distributions(records_by_batch: dict[str, list[dict]], all_records: list[dict]) -> dict:
    out = {"batches": {}, "combined": {}}
    for batch_name, batch_records in records_by_batch.items():
        out["batches"][batch_name] = {
            field: compute_distribution(batch_records, field) for field in KEY_FIELDS
        }
    out["combined"] = {field: compute_distribution(all_records, field) for field in KEY_FIELDS}
    return out


def compute_drift(records_by_batch: dict[str, list[dict]]) -> dict:
    batch_names = list(records_by_batch.keys())
    if len(batch_names) < 2:
        return {}
    left_name, right_name = batch_names[0], batch_names[1]
    left = records_by_batch[left_name]
    right = records_by_batch[right_name]
    drift = {"_comparison": {"left": left_name, "right": right_name}}
    for field in KEY_FIELDS:
        left_dist = compute_distribution(left, field)
        right_dist = compute_distribution(right, field)
        keys = set(left_dist["counts"]) | set(right_dist["counts"])
        rows = []
        for key in sorted(keys):
            l = left_dist["counts"].get(key, 0)
            r = right_dist["counts"].get(key, 0)
            rows.append(
                {
                    "label": key,
                    "left_count": l,
                    "left_pct": top_pct(l, len(left)),
                    "right_count": r,
                    "right_pct": top_pct(r, len(right)),
                    "pct_diff": round(top_pct(r, len(right)) - top_pct(l, len(left)), 2),
                }
            )
        rows.sort(key=lambda x: abs(x["pct_diff"]), reverse=True)
        drift[field] = rows
    return drift


def has_high_risk_label(rec: dict) -> bool:
    for field, labels in HIGH_RISK_LABELS.items():
        if rec.get(field) in labels:
            return True
    return False


def build_record_view(rec: dict, review_row: dict[str, str]) -> dict[str, str | int]:
    text = normalize_text(review_row)
    return {
        "review_id": rec["review_id"],
        "batch": rec["_batch"],
        "rating": review_row.get("rating", ""),
        "verified_purchase": review_row.get("verified_purchase", ""),
        "date": review_row.get("date", ""),
        "word_count": len(text.split()),
        "text": text,
        "purchase_type_normalized": rec.get("purchase_type_normalized", ""),
        "support_level_for_family_ai_brain_normalized": rec.get(
            "support_level_for_family_ai_brain_normalized", ""
        ),
        "unmet_need_normalized": rec.get("unmet_need_normalized", ""),
        "hire_job_normalized": rec.get("hire_job_normalized", ""),
        "coder_note": rec.get("coder_note", ""),
        "path": rec["_path"],
    }


def detect_risks(records: list[dict], reviews: dict[str, dict[str, str]]) -> dict[str, list[dict]]:
    buckets: defaultdict[str, list[dict]] = defaultdict(list)
    for name in RISK_BUCKET_NAMES:
        buckets[name]
    for rec in records:
        review_row = reviews[rec["review_id"]]
        view = build_record_view(rec, review_row)
        text = str(view["text"])
        wc = int(view["word_count"])
        coder_note = str(rec.get("coder_note") or "").strip()
        support = rec.get("support_level_for_family_ai_brain_normalized")
        purchase = rec.get("purchase_type_normalized")
        unmet = rec.get("unmet_need_normalized")

        if has_high_risk_label(rec) and not coder_note:
            buckets["high_risk_missing_coder_note"].append(view)

        if support == "screen_only" and FAMILY_STRONG_RE.search(text):
            buckets["screen_only_with_strong_family_signal"].append(view)
            if GIFT_CONTEXT_RE.search(text) and not OPERATIONAL_FAMILY_RE.search(text):
                buckets["screen_only_family_gift_context"].append(view)
            elif OPERATIONAL_FAMILY_RE.search(text):
                buckets["screen_only_family_operational_signal"].append(view)
            else:
                buckets["screen_only_family_mixed_or_other"].append(view)

        if support == "coordination_layer" and wc <= 8 and not FAMILY_STRONG_RE.search(text):
            if FAMILY_WEAK_RE.search(text) or not coder_note:
                buckets["coordination_layer_short_weak_evidence"].append(view)

        if support == "supports_family_ai_brain_core" and wc <= 12 and not FAMILY_STRONG_RE.search(text):
            buckets["supports_core_short_weak_evidence"].append(view)

        if (
            purchase == "tool_pain"
            and support == "screen_only"
            and wc <= 7
            and GENERIC_POSITIVE_RE.search(text)
            and not CONCRETE_TOOL_RE.search(text.replace("organized", ""))
        ):
            buckets["tool_pain_short_generic_positive"].append(view)

        if unmet == "unclear":
            buckets["unmet_unclear_all"].append(view)

        if purchase == "unclear" and wc <= 8:
            buckets["purchase_unclear_short"].append(view)

    return buckets


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["review_id"])
        return

    fieldnames = [
        "review_id",
        "batch",
        "rating",
        "verified_purchase",
        "date",
        "word_count",
        "purchase_type_normalized",
        "support_level_for_family_ai_brain_normalized",
        "unmet_need_normalized",
        "hire_job_normalized",
        "text",
        "coder_note",
        "path",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def format_top_rows(rows: list[dict], limit: int = 8) -> list[str]:
    out = []
    for row in rows[:limit]:
        out.append(
            f"- `{row['review_id']}` ({row['word_count']}词): "
            f"{row['purchase_type_normalized']} / "
            f"{row['support_level_for_family_ai_brain_normalized']} / "
            f"{row['unmet_need_normalized']} | {str(row['text'])[:120]}"
        )
    return out


def build_markdown(
    report_title: str,
    records: list[dict],
    batches: dict[str, Path],
    drift: dict,
    risks: dict[str, list[dict]],
) -> str:
    total = len(records)
    lines = [f"# {report_title}", "", f"日期：{date.today().isoformat()}", "", "## 审计范围", ""]
    lines.append(f"- 总样本：`{total}`")
    for batch_name, base in batches.items():
        lines.append(f"- `{batch_name}`: `{base}`")
    lines.append("")
    lines.append("## 核心结论")
    lines.append("")
    lines.append("- 技术完整性：请结合总数、final_out 条数和 missing_ids 判断。")
    lines.append(
        f"- `unmet_need_normalized=unclear` 当前 `{len(risks['unmet_unclear_all'])}` 条。"
    )
    lines.append(
        "- 主要内容风险通常集中在 support_level 的短评抬高、以及极短好评被过度判成 tool_pain。"
    )
    lines.append("")
    lines.append("## 关键风险桶")
    lines.append("")
    for key in RISK_BUCKET_NAMES:
        rows = risks[key]
        lines.append(f"### {key}")
        lines.append("")
        lines.append(f"- 数量：`{len(rows)}`")
        lines.extend(format_top_rows(rows))
        lines.append("")
    if drift:
        lines.append("## 分布漂移")
        lines.append("")
        comparison = drift.get("_comparison", {})
        lines.append(
            f"- 对比批次：`{comparison.get('left', '')}` -> `{comparison.get('right', '')}`"
        )
        lines.append("")
        for field in KEY_FIELDS:
            rows = drift.get(field, [])
            lines.append(f"### {field}")
            lines.append("")
            for row in rows[:8]:
                lines.append(
                    f"- `{row['label']}`: "
                    f"左批 `{row['left_pct']}%` ({row['left_count']}) -> "
                    f"右批 `{row['right_pct']}%` ({row['right_count']}); "
                    f"差值 `{row['pct_diff']} pct`"
                )
            lines.append("")
    lines.append("## 建议")
    lines.append("")
    lines.append(
        f"1. 优先复核 `coordination_layer_short_weak_evidence` 的 `{len(risks['coordination_layer_short_weak_evidence'])}` 条。"
    )
    lines.append(
        f"2. 再复核 `supports_core_short_weak_evidence` 的 `{len(risks['supports_core_short_weak_evidence'])}` 条。"
    )
    lines.append(
        f"3. 若要更严口径，再看 `tool_pain_short_generic_positive` 的 `{len(risks['tool_pain_short_generic_positive'])}` 条。"
    )
    lines.append("4. `unmet_need` 是否需要动，优先看 `unmet_unclear_all` 和 codebook 当前定义。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    review_csv = Path(args.review_csv)
    audit_dir = Path(args.audit_dir)
    batches = parse_batches(args.batch)
    report_title = args.report_title or "JTBD 结果系统审计"

    ensure_dir(audit_dir)
    reviews = load_reviews(review_csv)
    records = load_outputs(batches)
    records_by_batch: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        records_by_batch[rec["_batch"]].append(rec)

    distributions = summarize_distributions(records_by_batch, records)
    drift = compute_drift(records_by_batch)
    risks = detect_risks(records, reviews)

    for bucket_name, rows in risks.items():
        write_csv(audit_dir / f"{bucket_name}.csv", rows)

    summary = {
        "total_records": len(records),
        "batch_counts": {k: len(v) for k, v in records_by_batch.items()},
        "risk_bucket_counts": {k: len(v) for k, v in risks.items()},
        "distributions": distributions,
        "drift": drift,
        "audit_dir": str(audit_dir),
    }
    with (audit_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    markdown = build_markdown(report_title, records, batches, drift, risks)
    with (audit_dir / "report.md").open("w", encoding="utf-8") as f:
        f.write(markdown)

    print(
        json.dumps(
            {
                "total_records": len(records),
                "risk_bucket_counts": {k: len(v) for k, v in risks.items()},
                "audit_dir": str(audit_dir),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
