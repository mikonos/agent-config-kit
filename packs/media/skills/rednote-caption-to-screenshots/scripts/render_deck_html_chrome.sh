#!/usr/bin/env bash
set -euo pipefail

# Render deck HTML (#p01..#p0N) to 1080x1440 PNGs using local Chrome.
#
# ⚠️ WARNING: This method relies on CSS :target selectors, which are UNRELIABLE
# in Chrome headless mode. Pages P2-P8 may render as blank/white.
#
# RECOMMENDED: Use render_deck_playwright.js instead for stable results.
#
# If you must use this script, your HTML needs these CSS rules:
#   .page { display: none; }
#   .page:first-of-type { display: flex; }
#   .page:target { display: flex; }
#
# Usage:
#   scripts/render_deck_html_chrome.sh "<htmlPath>" "<outDir>" <pages> "<prefix>"
#
# Example:
#   scripts/render_deck_html_chrome.sh "./deck.html" "./out" 8 "20260126_topic"

HTML_PATH="${1:?htmlPath required}"
OUT_DIR="${2:?outDir required}"
PAGES="${3:?pages required}"
PREFIX="${4:?prefix required}"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$CHROME" ]]; then
  echo "Chrome not found at: $CHROME" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

FILE_URL="file://$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$HTML_PATH")"

pad2() { printf "%02d" "$1"; }

for ((i=1; i<=PAGES; i++)); do
  ii="$(pad2 "$i")"
  hi="${OUT_DIR}/${PREFIX}_@2x_p${ii}.png"
  lo="${OUT_DIR}/${PREFIX}_p${ii}.png"

  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=1080,1440 --virtual-time-budget=1200 \
    --screenshot="$hi" "${FILE_URL}#p${ii}" >/dev/null 2>&1

  /usr/bin/sips -Z 1440 "$hi" --out "$lo" >/dev/null 2>&1
  echo "OK: $lo"
done

