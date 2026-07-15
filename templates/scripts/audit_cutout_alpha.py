#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from PIL import Image


def components(mask: list[list[bool]], w: int, h: int) -> list[int]:
    seen = [[False] * w for _ in range(h)]
    sizes: list[int] = []
    for y in range(h):
        for x in range(w):
            if not mask[y][x] or seen[y][x]:
                continue
            q = deque([(x, y)])
            seen[y][x] = True
            n = 0
            while q:
                cx, cy = q.popleft()
                n += 1
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            sizes.append(n)
    return sorted(sizes, reverse=True)


def audit(path: Path) -> dict:
    im = Image.open(path).convert("RGBA")
    alpha = im.getchannel("A")
    w, h = im.size
    bbox = alpha.getbbox()
    opaque = sum(1 for v in alpha.getdata() if v > 20)
    semi = sum(1 for v in alpha.getdata() if 20 < v < 230)
    mask = []
    # Downsample for portable connected-component scan.
    small = alpha.resize((max(1, w // 4), max(1, h // 4)))
    sw, sh = small.size
    data = list(small.getdata())
    for y in range(sh):
        mask.append([data[y * sw + x] > 20 for x in range(sw)])
    comps = components(mask, sw, sh)
    small_islands = sum(1 for s in comps[1:] if s < 30)
    bbox_area = 0
    if bbox:
        bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    flags = []
    if len(comps) > 5:
        flags.append("many_alpha_islands")
    if small_islands > 2:
        flags.append("small_stray_islands")
    if bbox and bbox_area > 0 and opaque / bbox_area < 0.18:
        flags.append("sparse_large_bbox")
    if semi / max(1, opaque) > 0.55:
        flags.append("many_semitransparent_pixels")
    return {
        "file": str(path),
        "size": [w, h],
        "bbox": bbox,
        "opaque_pixels": opaque,
        "semi_pixels": semi,
        "components": comps[:8],
        "flags": flags,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_dir")
    parser.add_argument("--out", default="out/alpha-audit.json")
    args = parser.parse_args()
    root = Path(args.asset_dir)
    results = [audit(path) for path in sorted(root.rglob("*.png"))]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    flagged = [r for r in results if r["flags"]]
    print(f"audited={len(results)} flagged={len(flagged)} out={out}")
    for item in flagged[:12]:
        print(item["file"], item["flags"])


if __name__ == "__main__":
    main()
