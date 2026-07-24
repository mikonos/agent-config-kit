#!/usr/bin/env python3
"""Convert six coin-toss lines into a basic Liuyao hexagram.

Default convention:
- zheng / 正 = 3 points
- fan / 反 = 2 points
- 9 = old yang moving, 8 = young yin, 7 = young yang, 6 = old yin moving

Input order is bottom line to top line.
"""

from __future__ import annotations

import re
import sys


TRIGRAMS = {
    (1, 1, 1): "乾",
    (1, 1, 0): "兑",
    (1, 0, 1): "离",
    (1, 0, 0): "震",
    (0, 1, 1): "巽",
    (0, 1, 0): "坎",
    (0, 0, 1): "艮",
    (0, 0, 0): "坤",
}


HEXAGRAMS = {
    ("乾", "乾"): "1 乾为天",
    ("兑", "乾"): "10 天泽履",
    ("离", "乾"): "13 天火同人",
    ("震", "乾"): "25 天雷无妄",
    ("巽", "乾"): "44 天风姤",
    ("坎", "乾"): "6 天水讼",
    ("艮", "乾"): "33 天山遁",
    ("坤", "乾"): "12 天地否",
    ("乾", "兑"): "43 泽天夬",
    ("兑", "兑"): "58 兑为泽",
    ("离", "兑"): "49 泽火革",
    ("震", "兑"): "17 泽雷随",
    ("巽", "兑"): "28 泽风大过",
    ("坎", "兑"): "47 泽水困",
    ("艮", "兑"): "31 泽山咸",
    ("坤", "兑"): "45 泽地萃",
    ("乾", "离"): "14 火天大有",
    ("兑", "离"): "38 火泽睽",
    ("离", "离"): "30 离为火",
    ("震", "离"): "21 火雷噬嗑",
    ("巽", "离"): "50 火风鼎",
    ("坎", "离"): "64 火水未济",
    ("艮", "离"): "56 火山旅",
    ("坤", "离"): "35 火地晋",
    ("乾", "震"): "34 雷天大壮",
    ("兑", "震"): "54 雷泽归妹",
    ("离", "震"): "55 雷火丰",
    ("震", "震"): "51 震为雷",
    ("巽", "震"): "32 雷风恒",
    ("坎", "震"): "40 雷水解",
    ("艮", "震"): "62 雷山小过",
    ("坤", "震"): "16 雷地豫",
    ("乾", "巽"): "9 风天小畜",
    ("兑", "巽"): "61 风泽中孚",
    ("离", "巽"): "37 风火家人",
    ("震", "巽"): "42 风雷益",
    ("巽", "巽"): "57 巽为风",
    ("坎", "巽"): "59 风水涣",
    ("艮", "巽"): "53 风山渐",
    ("坤", "巽"): "20 风地观",
    ("乾", "坎"): "5 水天需",
    ("兑", "坎"): "60 水泽节",
    ("离", "坎"): "63 水火既济",
    ("震", "坎"): "3 水雷屯",
    ("巽", "坎"): "48 水风井",
    ("坎", "坎"): "29 坎为水",
    ("艮", "坎"): "39 水山蹇",
    ("坤", "坎"): "8 水地比",
    ("乾", "艮"): "26 山天大畜",
    ("兑", "艮"): "41 山泽损",
    ("离", "艮"): "22 山火贲",
    ("震", "艮"): "27 山雷颐",
    ("巽", "艮"): "18 山风蛊",
    ("坎", "艮"): "4 山水蒙",
    ("艮", "艮"): "52 艮为山",
    ("坤", "艮"): "23 山地剥",
    ("乾", "坤"): "11 地天泰",
    ("兑", "坤"): "19 地泽临",
    ("离", "坤"): "36 地火明夷",
    ("震", "坤"): "24 地雷复",
    ("巽", "坤"): "46 地风升",
    ("坎", "坤"): "7 地水师",
    ("艮", "坤"): "15 地山谦",
    ("坤", "坤"): "2 坤为地",
}


def parse_line(text: str) -> int:
    text = text.strip().lower()
    zheng = 0
    fan = 0

    for number, token in re.findall(r"([0-3])\s*(正|反|zheng|fan|heads?|tails?)", text):
        if token in {"正", "zheng", "head", "heads"}:
            zheng += int(number)
        else:
            fan += int(number)

    if not (zheng or fan):
        normalized = text.replace(" ", "")
        if normalized in {"3正", "正正正", "3zheng", "hhh"}:
            zheng = 3
        elif normalized in {"2正1反", "正正反", "2zheng1fan", "hht"}:
            zheng, fan = 2, 1
        elif normalized in {"1正2反", "正反反", "1zheng2fan", "htt"}:
            zheng, fan = 1, 2
        elif normalized in {"3反", "反反反", "3fan", "ttt"}:
            fan = 3

    if zheng + fan != 3:
        raise ValueError(f"invalid line {text!r}; expected three coins")
    return zheng * 3 + fan * 2


def line_info(value: int) -> tuple[int, bool, str]:
    if value == 9:
        return 1, True, "老阳动"
    if value == 8:
        return 0, False, "少阴静"
    if value == 7:
        return 1, False, "少阳静"
    if value == 6:
        return 0, True, "老阴动"
    raise ValueError(f"invalid coin sum {value}")


def hexagram_name(lines: list[int]) -> tuple[str, str, str]:
    lower = TRIGRAMS[tuple(lines[:3])]
    upper = TRIGRAMS[tuple(lines[3:])]
    return lower, upper, HEXAGRAMS[(lower, upper)]


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print('usage: coin_hexagram.py "3正" "2正1反" "1正2反" "3反" "2正1反" "1正2反"', file=sys.stderr)
        return 2

    values = [parse_line(arg) for arg in argv]
    infos = [line_info(value) for value in values]
    base_lines = [info[0] for info in infos]
    changed_lines = [1 - bit if moving else bit for bit, moving, _ in infos]
    moving = [str(i + 1) for i, (_, is_moving, _) in enumerate(infos) if is_moving]

    base_lower, base_upper, base_name = hexagram_name(base_lines)
    changed_lower, changed_upper, changed_name = hexagram_name(changed_lines)

    print("输入顺序：第1爻到第6爻，自下而上")
    for index, (value, (bit, is_moving, label)) in enumerate(zip(values, infos), 1):
        yin_yang = "阳" if bit else "阴"
        mark = "动" if is_moving else "静"
        print(f"第{index}爻：{value} = {label}（{yin_yang}爻，{mark}）")
    print(f"本卦：{base_name}（下{base_lower}上{base_upper}）")
    print(f"变卦：{changed_name}（下{changed_lower}上{changed_upper}）")
    print(f"动爻：{','.join(moving) if moving else '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
