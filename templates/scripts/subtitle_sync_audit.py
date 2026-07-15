#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def usage() -> None:
    print("Usage: python3 scripts/subtitle_sync_audit.py <captions.ts> <audio.wav>")


def duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], text=True))


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] == "--help":
        usage()
        return
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    audio = duration(Path(sys.argv[2]))
    starts = [int(x) for x in re.findall(r"startMs:\s*(\d+)", text)]
    ends = [int(x) for x in re.findall(r"endMs:\s*(\d+)", text)]
    if not starts or len(starts) != len(ends):
        raise SystemExit("No parseable cues or mismatched starts/ends")
    gaps = [starts[i] - ends[i - 1] for i in range(1, len(starts))]
    print(f"cues={len(starts)} first={starts[0]} last={ends[-1]} audioMs={round(audio*1000)} maxGap={max(gaps) if gaps else 0}")


if __name__ == "__main__":
    main()
