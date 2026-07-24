#!/usr/bin/env python3
"""build_radar.py — 把评分后的机会 JSON 渲染成交互式四象限雷达 HTML（确定性，单一数据源）。

为什么要脚本：原 YouMind 版雷达的数据写死在 HTML 里，容易和报告表格脱钩、且自相矛盾
（蓝海机会被画在低稀缺位置）。本脚本用 scoring-rubric.md 的公式统一计算机会分、颜色、坐标，
保证「雷达 = 报告表格 = 评分规则」三者永远一致。无第三方依赖。

输入 JSON（dict 或 list 皆可）：
{
  "title": "小众 AI 产品机会雷达图",
  "subtitle": "需求强度 × 供给稀缺度，气泡=B2C订阅适配度",
  "date": "2026-06-24",
  "opportunities": [
    {"id":"8","name":"AI问责伙伴","demand":95,"scarcity":90,"b2c_fit":10,"ai_fit":"高","stage":"概念验证期"},
    ...
  ]
}
- demand / scarcity: 0–100
- b2c_fit: 0–10
- ai_fit: "高" | "中" | "低"（也接受 high/medium/low）
- id / stage / name 可选；name 缺省由 id 生成

用法：
  python3 build_radar.py --in opps.json --out-html radar.html [--out-md-table table.md] \
     [--title T] [--subtitle S] [--date YYYY-MM-DD] [--template path]
"""
import argparse, json, os, sys

AI_MULT  = {"高": 1.0, "中": 0.7, "低": 0.4, "high": 1.0, "medium": 0.7, "low": 0.4}
AI_LABEL = {"高": "高", "中": "中", "低": "低", "high": "高", "medium": "中", "low": "低"}
AI_COLOR = {"高": "#22c55e", "中": "#eab308", "低": "#9ca3af"}

BAND = [(600, "🟢 黄金"), (400, "🟢 强"), (200, "🟡 观望"), (0, "⚪ 放弃")]


def band(score):
    for lo, label in BAND:
        if score >= lo:
            return label
    return "⚪ 放弃"


def opp_score(demand, scarcity, b2c_fit, ai_fit):
    """机会分 = (需求/100)×(稀缺/100)×(B2C/10)×AI系数 ×1000，四舍五入。"""
    mult = AI_MULT[ai_fit]
    return round((demand / 100) * (scarcity / 100) * (b2c_fit / 10) * mult * 1000)


def validate(o, idx):
    name = o.get("name") or f"#{o.get('id', idx+1)}"
    for k, lo, hi in [("demand", 0, 100), ("scarcity", 0, 100), ("b2c_fit", 0, 10)]:
        if k not in o:
            sys.exit(f"[错误] 机会「{name}」缺字段 {k}")
        if not (lo <= o[k] <= hi):
            sys.exit(f"[错误] 机会「{name}」字段 {k}={o[k]} 越界（应在 {lo}-{hi}）")
    if o.get("ai_fit") not in AI_MULT:
        sys.exit(f"[错误] 机会「{name}」ai_fit 应为 高/中/低，当前 {o.get('ai_fit')!r}")
    return name


def build_rows(opportunities):
    rows = []
    for i, o in enumerate(opportunities):
        name = validate(o, i)
        ai = o["ai_fit"]
        score = opp_score(o["demand"], o["scarcity"], o["b2c_fit"], ai)
        disp_id = str(o.get("id", i + 1))
        disp_name = name if name.startswith("#") else f"#{disp_id} {name}"
        rows.append({
            "name": disp_name,
            "x": o["demand"], "y": o["scarcity"], "b2c": o["b2c_fit"],
            "ai": AI_LABEL[ai], "score": score, "stage": o.get("stage", ""),
            "color": AI_COLOR[AI_LABEL[ai]],
        })
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def md_table(rows):
    out = ["| 机会 | X 需求 | Y 稀缺 | 气泡 B2C | AI | 机会分 | 分档 |",
           "|---|---|---|---|---|---|---|"]
    emoji = {"高": "🟢", "中": "🟡", "低": "⚪"}
    for r in rows:
        out.append(f"| {r['name']} | {r['x']} | {r['y']} | {r['b2c']} | {emoji[r['ai']]} | {r['score']} | {band(r['score'])} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="评分 JSON → 雷达 HTML（确定性）")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out-html", required=True)
    ap.add_argument("--out-md-table", default=None)
    ap.add_argument("--template", default=os.path.join(os.path.dirname(__file__), "..", "assets", "radar-chart-template.html"))
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--date", default=None)
    args = ap.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        data = json.load(f)
    meta = data if isinstance(data, dict) else {}
    opportunities = data["opportunities"] if isinstance(data, dict) else data
    if not opportunities:
        sys.exit("[错误] 没有机会数据")

    rows = build_rows(opportunities)

    title = args.title or meta.get("title", "小众 AI 产品机会雷达图")
    subtitle = args.subtitle or meta.get("subtitle", "需求强度 × 供给稀缺度，气泡 = B2C 订阅适配度")
    date = args.date or meta.get("date", "")

    with open(args.template, encoding="utf-8") as f:
        html = f.read()
    html = (html
            .replace("__RADAR_DATA__", json.dumps(rows, ensure_ascii=False))
            .replace("__RADAR_TITLE__", title)
            .replace("__RADAR_SUBTITLE__", subtitle)
            .replace("__SCAN_DATE__", date))

    with open(args.out_html, "w", encoding="utf-8") as f:
        f.write(html)

    table = md_table(rows)
    if args.out_md_table:
        with open(args.out_md_table, "w", encoding="utf-8") as f:
            f.write(table + "\n")

    print(f"✅ 雷达已生成：{args.out_html}（{len(rows)} 个机会）")
    print("排序后的机会分（与报告表格同源）：\n" + table)


if __name__ == "__main__":
    main()
