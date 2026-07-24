#!/usr/bin/env python3
"""Collect YouTube RSS/video subtitle evidence for radar reports.

The script intentionally emits evidence packets and a rough Markdown table.
The agent should still write the final judgment report in human language.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from pathlib import Path

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

USER_AGENT = {"User-Agent": "Mozilla/5.0"}

CHANNEL_WEIGHTS = {
    "OpenAI": 20,
    "Andrej Karpathy": 20,
    "Dwarkesh Patel": 19,
    "Stratechery": 18,
    "a16z": 18,
    "All-In Podcast": 17,
    "The Circuit": 17,
    "No Priors": 17,
    "Y Combinator": 16,
    "Invest Like The Best": 16,
    "Sequoia Capital": 16,
    "The AI Daily Brief": 16,
    "Lenny's Podcast": 16,
    "Asianometry": 15,
    "Lex Fridman": 15,
    "Bridgewater": 15,
    "Acquired": 15,
    "20VC": 14,
    "ARK Invest": 14,
    "Stripe": 14,
    "Nathan Lambert": 14,
    "Sharp Tech": 14,
}

SIGNAL_TERMS = """
ai openai llm agent agents inference token compute gpu nvidia chip data center
ipo revenue customer startup energy power semiconductor model training pricing
cost venture market company cloud enterprise stablecoin treasury
""".split()


def run(cmd: list[str], timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)


def fetch_url(url: str, timeout: int = 30) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=USER_AGENT), timeout=timeout).read()


def clean_channel_url(url: str) -> str:
    return re.sub(r"/(videos|featured|shorts|streams|community)$", "", url.rstrip("/"))


def read_channels(path: Path) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        urls = re.findall(r"https://www\.youtube\.com/[^\s)]+", line)
        if not urls:
            continue
        url = urls[0].rstrip(",")
        label = re.sub(r"https://www\.youtube\.com/[^\s)]+", "", line).strip(" -\t")
        pairs.append((label or url, url))
    return pairs


def channel_id_from_url(label: str, url: str) -> str | None:
    videos_url = clean_channel_url(url) + "/videos"
    try:
        proc = run(["yt-dlp", "--ignore-config", "--no-warnings", "--flat-playlist", "--playlist-end", "1", "--dump-json", videos_url], timeout=60)
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{"):
                data = json.loads(line)
                return data.get("playlist_channel_id") or data.get("playlist_id")
    except Exception:
        pass

    try:
        page = fetch_url(clean_channel_url(url), timeout=25).decode("utf-8", "ignore")
        match = re.search(r"feeds/videos\.xml\?channel_id=([^\"<>\\]+)", page)
        if match:
            return html.unescape(match.group(1))
        match = re.search(r'"channelId":"(UC[\w-]+)"', page)
        if match:
            return match.group(1)
    except Exception:
        return None
    return None


def latest_from_channel(pair: tuple[str, str]) -> dict:
    label, url = pair
    cid = channel_id_from_url(label, url)
    if not cid:
        return {"channel": label, "source_url": url, "error": "channel id not found"}
    feed = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    try:
        root = ET.fromstring(fetch_url(feed, timeout=30))
        channel = root.findtext("atom:title", default=label, namespaces=NS) or label
        entry = root.find("atom:entry", NS)
        if entry is None:
            return {"channel": channel, "source_url": url, "feed": feed, "error": "feed has no entries"}
        link = ""
        link_node = entry.find("atom:link", NS)
        if link_node is not None:
            link = link_node.attrib.get("href", "")
        desc = entry.findtext("media:group/media:description", default="", namespaces=NS) or ""
        desc = re.sub(r"\s+", " ", desc).strip()
        return {
            "channel": channel,
            "source_name": label,
            "source_url": url,
            "feed": feed,
            "title": entry.findtext("atom:title", default="", namespaces=NS) or "",
            "published": (entry.findtext("atom:published", default="", namespaces=NS) or "")[:10],
            "url": link,
            "type": "Short" if "/shorts/" in link else "Video",
            "rss_summary": desc[:240],
        }
    except Exception as exc:
        return {"channel": label, "source_url": url, "feed": feed, "error": str(exc)}


def parse_report(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict] = []
    seen: set[str] = set()
    row_re = re.compile(
        r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(Video|Short)\s*\|\s*"
        r"\[(.*)\]\((https://www\.youtube\.com/(?:watch\?v=|shorts/)[^)]+)\)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
    )
    for line in text.splitlines():
        match = row_re.match(line)
        if not match:
            continue
        url = match.group(6)
        if url in seen:
            continue
        rows.append(
            {
                "score": int(match.group(1)),
                "channel": match.group(2),
                "published": match.group(3),
                "type": match.group(4),
                "title": match.group(5),
                "url": url,
                "rss_summary": match.group(7),
                "status": match.group(8),
            }
        )
        seen.add(url)
    return rows


def score_item(item: dict) -> dict:
    text = f"{item.get('title', '')} {item.get('rss_summary', '')}".lower()
    signal = min(35, sum(4 for term in SIGNAL_TERMS if term in text))
    source_weight = 10
    channel = item.get("channel", "")
    for key, weight in CHANNEL_WEIGHTS.items():
        if key.lower() in channel.lower():
            source_weight = weight
            break
    type_adj = -8 if item.get("type") == "Short" else 0
    item["score"] = int(max(0, min(100, 45 + signal + source_weight + type_adj - 10)))
    if item["score"] >= 80:
        item["action"] = "watch-now"
    elif item["score"] >= 70:
        item["action"] = "queue"
    elif item["score"] >= 55:
        item["action"] = "archive-summary"
    else:
        item["action"] = "skip"
    return item


def pick_caption(captions: dict) -> tuple[str | None, str | None, str | None]:
    for lang in ["en-orig", "en", "en-US", "en-GB", "zh-Hans", "zh-Hant"]:
        if lang not in captions:
            continue
        for wanted in ["json3", "vtt", "srv3", "ttml"]:
            for fmt in captions[lang]:
                if fmt.get("ext") == wanted and fmt.get("url"):
                    return lang, fmt["url"], fmt.get("ext")
    for lang, formats in captions.items():
        for wanted in ["json3", "vtt"]:
            for fmt in formats:
                if fmt.get("ext") == wanted and fmt.get("url"):
                    return lang, fmt["url"], fmt.get("ext")
    return None, None, None


def parse_json3(data: str) -> list[tuple[float, str]]:
    obj = json.loads(data)
    segments: list[tuple[float, str]] = []
    for event in obj.get("events", []):
        if "segs" not in event:
            continue
        text = "".join(seg.get("utf8", "") for seg in event.get("segs", [])).strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            segments.append((event.get("tStartMs", 0) / 1000, text))
    return segments


def parse_vtt(data: str) -> list[tuple[float, str]]:
    segments: list[tuple[float, str]] = []
    for block in re.split(r"\n\s*\n", data):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        idx = 0 if "-->" in lines[0] else 1
        if idx >= len(lines) or "-->" not in lines[idx]:
            continue
        start = lines[idx].split("-->")[0].strip()
        match = re.match(r"(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)", start)
        seconds = 0.0
        if match:
            seconds = int(match.group(1) or 0) * 3600 + int(match.group(2)) * 60 + float(match.group(3))
        body = " ".join(lines[idx + 1 :])
        body = html.unescape(re.sub(r"<[^>]+>", " ", body))
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            segments.append((seconds, body))
    clean: list[tuple[float, str]] = []
    prev = ""
    for seconds, text in segments:
        if text != prev:
            clean.append((seconds, text))
            prev = text
    return clean


def format_ts(seconds: float) -> str:
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


def evidence_chunks(segments: list[tuple[float, str]]) -> list[dict]:
    chunks: list[tuple[float, str]] = []
    current: list[str] = []
    start: float | None = None
    size = 0
    for seconds, text in segments:
        if start is None:
            start = seconds
        current.append(text)
        size += len(text)
        if size >= 330 or seconds - start >= 24:
            chunks.append((start, re.sub(r"\s+", " ", " ".join(current)).strip()))
            current, start, size = [], None, 0
    if current:
        chunks.append((start or 0, re.sub(r"\s+", " ", " ".join(current)).strip()))

    scored: list[tuple[int, float, str]] = []
    for seconds, text in chunks:
        low = text.lower()
        score = sum(3 for term in SIGNAL_TERMS if term in low)
        score += len(re.findall(r"\b[A-Z][A-Za-z0-9&.-]{2,}\b", text))
        scored.append((score, seconds, text))

    chosen: list[tuple[float, str]] = chunks[:1]
    for _, seconds, text in sorted(scored, reverse=True)[:5]:
        if all(abs(seconds - existing[0]) > 45 for existing in chosen):
            chosen.append((seconds, text))
        if len(chosen) >= 4:
            break
    return [{"ts": format_ts(seconds), "text": text[:420]} for seconds, text in sorted(chosen, key=lambda item: item[0])[:4]]


def enrich_video(item: dict, subtitle_mode: str) -> dict:
    item = dict(item)
    item.update({"subtitle_source": "none", "subtitle_lang": "", "transcript_chars": 0, "evidence": [], "error": item.get("error", "")})
    if item.get("error") or not item.get("url"):
        return item
    try:
        proc = run(["yt-dlp", "--ignore-config", "--no-warnings", "--skip-download", "--dump-json", item["url"]], timeout=100)
        if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
            item["error"] = (proc.stderr or proc.stdout)[:500]
            return item
        meta = json.loads(proc.stdout)
        item["duration_string"] = meta.get("duration_string") or ""
        item["description"] = re.sub(r"\s+", " ", meta.get("description") or "").strip()[:1200]
        if subtitle_mode == "none":
            return item
        source = "manual"
        lang, caption_url, ext = pick_caption(meta.get("subtitles") or {})
        if not caption_url:
            source = "auto"
            lang, caption_url, ext = pick_caption(meta.get("automatic_captions") or {})
        if not caption_url:
            return item
        raw = fetch_url(caption_url, timeout=45).decode("utf-8", "ignore")
        segments = parse_json3(raw) if ext == "json3" else parse_vtt(raw)
        full = re.sub(r"\s+", " ", " ".join(text for _, text in segments)).strip()
        if len(full) < 80:
            item["error"] = "subtitle too short"
            return item
        item["subtitle_source"] = source
        item["subtitle_lang"] = lang or ""
        item["transcript_chars"] = len(full)
        item["evidence"] = evidence_chunks(segments)
    except Exception as exc:
        item["error"] = str(exc)[:500]
    return item


def confidence(item: dict) -> str:
    if item.get("subtitle_source") == "manual":
        return "high"
    if item.get("subtitle_source") == "auto":
        return "medium" if item.get("type") != "Short" else "medium-low"
    if item.get("description") or item.get("rss_summary"):
        return "low"
    return "very-low"


def rough_summary(item: dict) -> str:
    if item.get("description"):
        text = item["description"]
    elif item.get("rss_summary"):
        text = item["rss_summary"]
    elif item.get("evidence"):
        text = item["evidence"][0]["text"]
    else:
        text = "No summary source available."
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:180] + ("..." if len(text) > 180 else "")


def write_markdown(items: list[dict], output: Path, run_date: str, source: str) -> None:
    stats = Counter(item.get("subtitle_source", "none") for item in items)
    lines = [
        "---",
        f"date: {run_date}",
        "source_skill: youtube-video-radar",
        "epistemic_status: borrowed",
        "description: YouTube video radar evidence packet generated from RSS and subtitles.",
        "type: Intelligence_Radar",
        "tags: [video-radar, youtube]",
        "title: YouTube Video Radar Evidence Packet",
        "---",
        "",
        "# YouTube Video Radar Evidence Packet",
        "",
        "## System Log",
        "",
        f"- Source: {source}",
        f"- Input items: {len(items)}",
        f"- Manual subtitles: {stats.get('manual', 0)}",
        f"- Automatic subtitles: {stats.get('auto', 0)}",
        f"- No subtitles: {stats.get('none', 0)}",
        "",
        "## Evidence Table",
        "",
        "| Score | Channel | Date | Type | Title | Subtitle | Confidence | Rough summary | Evidence |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for item in sorted(items, key=lambda row: int(row.get("score", 0)), reverse=True):
        ev = " / ".join(chunk["ts"] for chunk in item.get("evidence", [])) or "RSS/description"
        title = f"[{item.get('title', '')}]({item.get('url', '')})"
        subtitle = item.get("subtitle_source", "none")
        if item.get("subtitle_lang"):
            subtitle += f"/{item['subtitle_lang']}"
        row = [
            str(item.get("score", "")),
            item.get("channel", ""),
            item.get("published", ""),
            item.get("type", ""),
            title,
            subtitle,
            confidence(item),
            rough_summary(item),
            ev,
        ]
        lines.append("| " + " | ".join(str(cell).replace("|", "/").replace("\n", " ") for cell in row) + " |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build YouTube radar evidence from channels or an existing report.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--channels-file", type=Path)
    source.add_argument("--from-report", type=Path)
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"))
    parser.add_argument("--subtitle-mode", choices=["none", "all"], default="none")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path)
    args = parser.parse_args()

    if args.channels_file:
        pairs = read_channels(args.channels_file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            items = list(executor.map(latest_from_channel, pairs))
        items = [score_item(item) if not item.get("error") else item for item in items]
        source_label = str(args.channels_file)
    else:
        items = parse_report(args.from_report)
        source_label = str(args.from_report)

    if args.limit:
        items = items[: args.limit]

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        items = list(executor.map(lambda item: enrich_video(item, args.subtitle_mode), items))

    args.out_json.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.out_md:
        write_markdown(items, args.out_md, args.date, source_label)

    stats = Counter(item.get("subtitle_source", "none") for item in items)
    print(json.dumps({"items": len(items), "subtitle_stats": dict(stats), "out_json": str(args.out_json), "out_md": str(args.out_md) if args.out_md else None}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
