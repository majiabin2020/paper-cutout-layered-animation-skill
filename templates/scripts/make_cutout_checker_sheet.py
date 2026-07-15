#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from PIL import Image, ImageDraw


def usage() -> None:
    print("Usage: python3 scripts/make_cutout_checker_sheet.py <asset-dir> <out.jpg>")


def checker(size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", size, (230, 230, 220, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, size[1], 18):
        for x in range(0, size[0], 18):
            if (x // 18 + y // 18) % 2:
                d.rectangle([x, y, x + 17, y + 17], fill=(200, 200, 190, 255))
    return img


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] == "--help":
        usage()
        return
    root = Path(sys.argv[1])
    out = Path(sys.argv[2])
    paths = sorted([*root.rglob("*.png"), *root.rglob("*.webp")])
    thumbs = []
    for path in paths:
        im = Image.open(path).convert("RGBA")
        bbox = im.getbbox()
        crop = im.crop(bbox) if bbox else im
        crop.thumbnail((220, 170))
        tile = checker((260, 230))
        tile.alpha_composite(crop, ((260 - crop.width) // 2, 24))
        d = ImageDraw.Draw(tile)
        d.rectangle([0, 0, 259, 229], outline=(80, 80, 70, 255), width=1)
        d.text((8, 202), path.relative_to(root).as_posix()[:36], fill=(20, 20, 20, 255))
        thumbs.append(tile.convert("RGB"))
    cols = 4
    rows = max(1, (len(thumbs) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * 260, rows * 230), (245, 242, 230))
    for i, tile in enumerate(thumbs):
        sheet.paste(tile, ((i % cols) * 260, (i // cols) * 230))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
