#!/usr/bin/env python3
"""Generate project issue launch-risk reports from GitHub issues."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import subprocess
import sys
from typing import Any


ISSUE_FIELDS = (
    "number,title,state,stateReason,labels,author,createdAt,updatedAt,closedAt,url"
)
TZ = dt.timezone(dt.timedelta(hours=8))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a product-launch issue report for a GitHub repo."
    )
    parser.add_argument("--repo", default="sunsetyyun/project", help="owner/repo")
    parser.add_argument("--days", type=int, default=9, help="trend window in days")
    parser.add_argument(
        "--format",
        choices=["feishu", "markdown"],
        default="feishu",
        help="output style",
    )
    parser.add_argument(
        "--timezone",
        default="Asia/Shanghai",
        help="display timezone label; calculations use UTC+8",
    )
    return parser.parse_args()


def run_gh(repo: str) -> list[dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "list",
        "-R",
        repo,
        "--state",
        "all",
        "--limit",
        "1000",
        "--json",
        ISSUE_FIELDS,
    ]
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    except FileNotFoundError:
        raise SystemExit("gh command not found")
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise SystemExit(f"gh issue list failed: {stderr or exc}") from exc
    return json.loads(result.stdout)


def labels(issue: dict[str, Any]) -> list[str]:
    return [item["name"] for item in issue.get("labels", [])]


def first_label(issue: dict[str, Any], candidates: set[str], default: str) -> str:
    for label in labels(issue):
        if label in candidates:
            return label
    return default


def priority(issue: dict[str, Any]) -> str:
    for label in labels(issue):
        if label.startswith("P") and len(label) == 2 and label[1:].isdigit():
            return label
    return "P?"


def areas(issue: dict[str, Any]) -> list[str]:
    return [label for label in labels(issue) if label.startswith("area:")]


def issue_type(issue: dict[str, Any]) -> str:
    for label in labels(issue):
        if label in {"bug", "enhancement", "product", "documentation"}:
            return label
    return "untyped"


def to_local_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ).date()


def date_window(issues: list[dict[str, Any]], days: int) -> list[dt.date]:
    today = dt.datetime.now(TZ).date()
    earliest = min((to_local_date(i["createdAt"]) for i in issues), default=today)
    start = max(earliest or today, today - dt.timedelta(days=days - 1))
    return [start + dt.timedelta(days=idx) for idx in range((today - start).days + 1)]


def trend_rows(issues: list[dict[str, Any]], days: int) -> list[dict[str, Any]]:
    rows = []
    for day in date_window(issues, days):
        opened = sum(1 for issue in issues if to_local_date(issue["createdAt"]) == day)
        closed = sum(1 for issue in issues if to_local_date(issue.get("closedAt")) == day)
        backlog = 0
        for issue in issues:
            created = to_local_date(issue["createdAt"])
            closed_at = to_local_date(issue.get("closedAt"))
            if created and created <= day and (closed_at is None or closed_at > day):
                backlog += 1
        rows.append({"date": day, "opened": opened, "closed": closed, "backlog": backlog})
    return rows


def sort_open(issue: dict[str, Any]) -> tuple[str, int, int]:
    status_order = {"待验收": 0, "待确认": 1, "无流程标签": 2}
    status = first_label(issue, {"待确认", "待验收"}, "无流程标签")
    return (priority(issue), status_order.get(status, 9), issue["number"])


def issue_line(issue: dict[str, Any]) -> str:
    return f"#{issue['number']} {issue['title']}"


def build_report(issues: list[dict[str, Any]], repo: str, days: int, display_tz: str) -> str:
    open_issues = [issue for issue in issues if issue["state"] == "OPEN"]
    closed_issues = [issue for issue in issues if issue["state"] == "CLOSED"]
    open_priorities = collections.Counter(priority(issue) for issue in open_issues)
    open_status = collections.Counter(
        first_label(issue, {"待确认", "待验收"}, "无流程标签")
        for issue in open_issues
    )
    open_areas = collections.Counter(
        area for issue in open_issues for area in areas(issue)
    )

    p0 = [issue for issue in open_issues if priority(issue) == "P0"]
    p1 = [issue for issue in open_issues if priority(issue) == "P1"]
    p1_by_area: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for issue in p1:
        issue_areas = areas(issue) or ["area: 未标"]
        for area in issue_areas:
            p1_by_area[area].append(issue)

    rows = trend_rows(issues, days)

    lines: list[str] = [
        "## project Issue 上线状态简报",
        "",
        f"仓库：{repo}",
        f"统计口径：{display_tz}，最近 {len(rows)} 天",
        "",
        "从产品上线角度看，当前重点不是继续开新需求，而是收口阻塞风险。",
        "",
        "**当前状态**",
        f"- 总 issue：{len(issues)}",
        f"- Open：{len(open_issues)}",
        f"- Closed：{len(closed_issues)}",
        f"- Open 中 P0：{open_priorities.get('P0', 0)}",
        f"- Open 中 P1：{open_priorities.get('P1', 0)}",
        f"- 待验收：{open_status.get('待验收', 0)}",
        f"- 待确认：{open_status.get('待确认', 0)}",
        f"- 无流程标签：{open_status.get('无流程标签', 0)}",
        "",
        "**上线阻塞**",
    ]

    if p0:
        lines.append("优先收口 P0：")
        for issue in sorted(p0, key=sort_open):
            lines.append(f"- {issue_line(issue)}")
    else:
        lines.append("当前没有打开的 P0。")

    lines.extend(["", "**P1 风险集中区**"])
    for area, grouped in open_areas.most_common(8):
        grouped_p1 = [issue for issue in p1_by_area.get(area, [])]
        if not grouped_p1:
            continue
        nums = "、".join(f"#{issue['number']}" for issue in sorted(grouped_p1, key=sort_open))
        lines.append(f"- {area.replace('area: ', '')}：{nums}")

    lines.extend(["", "**近期趋势**"])
    for row in rows:
        day = row["date"].strftime("%-m/%-d") if sys.platform != "win32" else row["date"].strftime("%m/%d").lstrip("0").replace("/0", "/")
        lines.append(
            f"{day} Open {row['backlog']} / 新开 {row['opened']} / 关闭 {row['closed']}"
        )

    lines.extend(
        [
            "",
            "**下一步**",
            "先清 P0；再把待验收转为通过或重开；最后把待确认判定为 MVP 内、MVP 后或研究项。",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    issues = run_gh(args.repo)
    print(build_report(issues, args.repo, args.days, args.timezone))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
