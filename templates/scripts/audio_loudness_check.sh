#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  echo "Usage: bash scripts/audio_loudness_check.sh"
  exit 0
fi

for file in out/*.mp4; do
  [[ -f "$file" ]] || continue
  echo "== audio $file =="
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels,duration -of default=nw=1 "$file"
  ffmpeg -v error -i "$file" -af astats=metadata=1:reset=1 -f null - 2>&1 | tail -n 12 || true
done
