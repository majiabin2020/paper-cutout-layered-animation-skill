#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageChops, ImageStat


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--out", default="out/motion-density.csv")
    parser.add_argument("--fps", default="2")
    args = parser.parse_args()
    video = Path(args.video)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        frame_pattern = Path(td) / "frame-%04d.jpg"
        subprocess.check_call(
            ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", f"fps={args.fps},scale=270:-1", str(frame_pattern)]
        )
        frames = sorted(Path(td).glob("frame-*.jpg"))
        rows = []
        prev = None
        for i, frame in enumerate(frames):
            im = Image.open(frame).convert("RGB")
            score = 0.0
            if prev is not None:
                diff = ImageChops.difference(prev, im)
                stat = ImageStat.Stat(diff)
                score = sum(stat.mean) / 3
            rows.append({"sample": i, "diff": round(score, 3), "status": "low" if i > 0 and score < 1.4 else "ok"})
            prev = im
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sample", "diff", "status"])
        writer.writeheader()
        writer.writerows(rows)
    lows = sum(1 for r in rows if r["status"] == "low")
    print(f"{video}: samples={len(rows)} low_motion={lows} out={out}")


if __name__ == "__main__":
    main()
