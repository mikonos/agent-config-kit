#!/usr/bin/env python3
"""
corpus_stats.py — Phase 6.5 & Phase 8 统计脚本
用途：读取所有星级 Structured CSV，输出字段非空率、信号类型分布、四力热力图、
      竞品提及、feature 频次、raw_job 频次等统计，供批次一致性简报和 QuantAnalysis 使用。

用法：
    python3 corpus_stats.py [CSV目录] [品类名]
    python3 corpus_stats.py . 日历机

输出：打印各统计结果到 stdout，可重定向到文件。
"""

import csv
import collections
import re
import sys
import os
from pathlib import Path


def safe(v):
    return (v or '').strip()


def split_multi(v):
    """分号分隔的多值字段切分，过滤空串"""
    return [x.strip() for x in safe(v).split(';') if x.strip()]


def load_csvs(directory, pattern='JTBD_Structured_*.csv'):
    """加载目录下所有星级 CSV，返回 {star: [rows]} 字典"""
    data = {}
    p = Path(directory)
    for fpath in sorted(p.glob(pattern)):
        m = re.search(r'(\d)star', fpath.name)
        if not m:
            continue
        star = int(m.group(1))
        rows = []
        with open(fpath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        data[star] = rows
        print(f"  已加载 {fpath.name}: {len(rows)} 条", file=sys.stderr)
    return data


def field_fill_rate(data):
    """各字段非空率（按星级）"""
    fields = [
        'force_push', 'force_pull', 'force_anxiety', 'force_habit',
        'raw_job_satisfied', 'raw_job_frustrated',
        'feature_satisfied', 'feature_implemented_frustrated', 'feature_requested',
        'competitor_mentions', 'anxiety_theme', 'signal_type'
    ]
    print("\n=== 字段非空率（Phase 6.5 批次一致性检查）===")
    header = "| 字段 | " + " | ".join(f"{s}★" for s in sorted(data.keys())) + " |"
    sep = "|------|" + "------|" * len(data)
    print(header)
    print(sep)
    for field in fields:
        row_vals = []
        for star in sorted(data.keys()):
            rows = data[star]
            n = len(rows)
            filled = sum(1 for r in rows if safe(r.get(field)))
            row_vals.append(f"{filled/n*100:.0f}%")
        print(f"| {field} | " + " | ".join(row_vals) + " |")


def signal_type_dist(data):
    """信号类型分布 × 星级"""
    print("\n=== 信号类型分布 × 星级 ===")
    for star in sorted(data.keys()):
        rows = data[star]
        n = len(rows)
        counter = collections.Counter()
        for r in rows:
            for t in split_multi(r.get('signal_type')):
                counter[t] += 1
        print(f"\n  {star}★ (n={n}):")
        for k, v in counter.most_common():
            print(f"    {k}: {v} ({v/n*100:.0f}%)")


def forces_heatmap(data):
    """四力热力图 × 星级"""
    force_fields = ['force_push', 'force_pull', 'force_anxiety', 'force_habit']
    force_labels = {'force_push': 'Push', 'force_pull': 'Pull',
                    'force_anxiety': 'Anxiety', 'force_habit': 'Habit'}
    print("\n=== 四力分布热力图 × 星级 ===")
    print("| 星级 | Push | Pull | Anxiety | Habit |")
    print("|------|------|------|---------|-------|")
    for star in sorted(data.keys()):
        rows = data[star]
        n = len(rows)
        vals = []
        for ff in force_fields:
            c = sum(1 for r in rows if safe(r.get(ff)))
            vals.append(f"{c}({c/n*100:.0f}%)")
        print(f"| {star}★ (n={n}) | " + " | ".join(vals) + " |")


def competitor_analysis(data):
    """竞品提及频次（全量合并）"""
    counter = collections.Counter()
    for rows in data.values():
        for r in rows:
            for item in split_multi(r.get('competitor_mentions')):
                if item.lower() not in ('none', '无', ''):
                    counter[item] += 1
    print("\n=== 竞品提及 Top 20 ===")
    for k, v in counter.most_common(20):
        print(f"  {v:4d}  {k}")


def anxiety_themes(data):
    """焦虑主题频次（过滤 signal_type 噪声）"""
    noise = {'hire_moment', 'fire_moment', 'workaround', 'wishlist'}
    counter = collections.Counter()
    for rows in data.values():
        for r in rows:
            for item in split_multi(r.get('anxiety_theme')):
                if item.lower() not in noise:
                    counter[item] += 1
    print("\n=== 焦虑主题 Top 20（已过滤 signal_type 噪声）===")
    for k, v in counter.most_common(20):
        print(f"  {v:4d}  {k}")


def feature_stats(data):
    """Feature 三类频次统计"""
    sat = collections.Counter()
    impl_if = collections.Counter()
    req = collections.Counter()
    for rows in data.values():
        for r in rows:
            for v in split_multi(r.get('feature_satisfied')):
                sat[v] += 1
            for v in split_multi(r.get('feature_implemented_frustrated')):
                impl_if[v] += 1
            for v in split_multi(r.get('feature_requested')):
                req[v] += 1
    print("\n=== Feature Satisfied Top 30 ===")
    for k, v in sat.most_common(30):
        print(f"  {v:4d}  {k}")
    print("\n=== Feature Impl_Frustrated Top 20 ===")
    for k, v in impl_if.most_common(20):
        print(f"  {v:4d}  {k}")
    print("\n=== Feature Requested Top 20 ===")
    for k, v in req.most_common(20):
        print(f"  {v:4d}  {k}")


def raw_job_stats(data):
    """raw_job satisfied/frustrated 频次统计"""
    sat = collections.Counter()
    fri = collections.Counter()
    for rows in data.values():
        for r in rows:
            for v in split_multi(r.get('raw_job_satisfied')):
                sat[v] += 1
            for v in split_multi(r.get('raw_job_frustrated')):
                fri[v] += 1
    print("\n=== Raw Job Satisfied Top 20 ===")
    for k, v in sat.most_common(20):
        print(f"  {v:4d}  {k}")
    print("\n=== Raw Job Frustrated Top 20 ===")
    for k, v in fri.most_common(20):
        print(f"  {v:4d}  {k}")


def row_counts(data):
    """各星级行数汇总"""
    print("\n=== 条数核对 ===")
    total = 0
    for star in sorted(data.keys()):
        n = len(data[star])
        total += n
        print(f"  {star}★: {n}")
    print(f"  合计: {total}")


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    category = sys.argv[2] if len(sys.argv) > 2 else '品类'

    print(f"=== JTBD Amazon Corpus Stats · {category} ===")
    print(f"目录：{os.path.abspath(directory)}\n")

    data = load_csvs(directory)
    if not data:
        print("未找到符合条件的 CSV 文件（JTBD_Structured_*star.csv）")
        sys.exit(1)

    row_counts(data)
    field_fill_rate(data)
    signal_type_dist(data)
    forces_heatmap(data)
    competitor_analysis(data)
    anxiety_themes(data)
    feature_stats(data)
    raw_job_stats(data)


if __name__ == '__main__':
    main()
