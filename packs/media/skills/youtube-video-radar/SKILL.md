---
name: youtube-video-radar
description: Build YouTube channel radar reports from RSS and subtitles. Use this skill whenever the user asks what many YouTube/podcast channels recently published, wants a daily/weekly video radar, asks to rank which videos to watch, wants subtitle-backed summaries, or wants to turn a list of YouTube channels/videos into a Zettelkasten-ready intelligence report.
---

# YouTube Video Radar

Use this skill to turn a pile of YouTube channels or video links into a small number of watch decisions. The job is not to consume everything; it is to make the user's attention allocation explicit.

## Core Workflow

1. **Define the scope**
   - If the user gives channel URLs, build a latest-video radar from those channels.
   - If the user points to an existing radar report, upgrade it with subtitle evidence.
   - If the user asks "what should I watch", rank by subtitle-confirmed signal, not by RSS title alone.

2. **Collect evidence with the script**
   - For channels:
     ```bash
     python "<installed-skill-dir>/scripts/youtube_radar.py" \
       --channels-file <channels.txt> \
       --date YYYYMMDD \
       --subtitle-mode none \
       --out-json /tmp/youtube_radar_YYYYMMDD.json \
       --out-md /tmp/youtube_radar_YYYYMMDD.md
     ```
   - For subtitle upgrade from an existing Markdown report:
     ```bash
     python "<installed-skill-dir>/scripts/youtube_radar.py" \
       --from-report <report.md> \
       --date YYYYMMDD \
       --subtitle-mode all \
       --out-json /tmp/youtube_radar_subtitles_YYYYMMDD.json \
       --out-md /tmp/youtube_radar_subtitles_YYYYMMDD.md
     ```

3. **Write the human report**
   - Use `references/report-template.md` as the report shape.
   - Do not paste full transcripts into the vault. Keep only subtitle source, confidence, concise summary, and evidence timestamps.
   - If subtitles are unavailable, label the row as RSS/description fallback.

4. **Rank Top 5**
   Rank by:
   - Connection to the user's current themes: AI economics, inference, agent systems, business models, investing, energy/compute constraints.
   - Evidence quality: manual subtitle > automatic subtitle > official description > title-only.
   - Decision value: whether the video changes a belief or action, not whether it is merely interesting.
   - Freshness and source quality.

5. **Zettelkasten handling**
   - Default to conversational output. Write a report only when the user authorizes a target path that follows the current project's note conventions.
   - Link only to indexes that actually exist in the target Vault; do not invent maintainer-specific links.
   - Do not auto-generate atomic notes from every video. Suggest at most 1-3 atomic candidates after the report.
   - Write an open loop only if the user must choose or do something next. Remove stale open loops once the user chooses.

## Output Principles

- Say clearly which layer produced each summary: RSS, official description, automatic subtitle, manual subtitle, or full deep read.
- Treat automatic captions as medium confidence. They often mangle names, acronyms, and numbers.
- For Shorts, keep summaries short and usually lower priority unless the subtitle reveals a strong signal.
- For very long videos, use subtitle evidence to decide whether to deep-read; do not deep-read all long videos by default.

## Validation

Before finishing:

- Confirm the input count and output count match.
- Confirm subtitle statistics are reported: manual / auto / none.
- Check the report has a Top 5 or an explicit reason why no Top 5 is possible.
- Check no full transcript text was written to the vault.
