#!/bin/bash
# get_random_notes.sh
# Extract random notes based on the specified mode for the random-walk skill.
# Usage: ./get_random_notes.sh --mode <mode> [--count <count>]

MODE=""
COUNT=1

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --mode) MODE="$2"; shift ;;
        --count) COUNT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [[ -z "$MODE" ]]; then
    echo "Error: --mode is required."
    exit 1
fi

case "$MODE" in
    tension)
        # Select n semantically distant notes using seed-based random sampling
        SEED=$(date +%s)
        find "05_每日记录" "longlongago" -name "*.md" -type f 2>/dev/null | \
            awk -v seed=$SEED 'BEGIN{srand(seed)} {print rand() "\t" $0}' | \
            sort -n | cut -f2- | head -n "$COUNT"
        ;;
    forgotten)
        # Select n notes > 90 days old with <= 1 incoming links
        find "05_每日记录" "longlongago" -type f -name "*.md" -mtime +90 2>/dev/null | while read -r file; do
            # Check link count
            basename=$(basename "$file" .md)
            # count links in 05 and 03
            link_count=$(grep -rc "\[\[$basename\]\]" "05_每日记录" "03_索引" 2>/dev/null | awk -F: '{sum+=$2} END{print sum+0}')
            if [ "$link_count" -le 1 ]; then
                echo "$file"
            fi
        done | head -n 50 | sort -R | head -n "$COUNT"
        ;;
    recent)
        # Select n recent notes (<= 7 days old)
        # Using sort -r to get the most recent ones if needed, or just random from recent
        find "05_每日记录" -type f -name "*.md" -mtime -7 2>/dev/null | sort -R | head -n "$COUNT"
        ;;
    *)
        echo "Error: Unknown mode '$MODE'. Supported modes: tension, forgotten, recent."
        exit 1
        ;;
esac
