#!/usr/bin/env python3
"""Create a Remotion project for layered paper-cutout videos."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import textwrap
import wave


def write(path: Path, content: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | 0o755)


def write_silence(path: Path, seconds: float, sample_rate: int = 24000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(seconds * sample_rate)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00" * frames)


def svg(width: int, height: int, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#f5efe2"/>
  <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0.18"/><feBlend mode="multiply" in2="SourceGraphic"/></filter>
  <g filter="url(#paper)">{body}</g>
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", default="Paper Cutout Story")
    parser.add_argument("--theme", default="a layered paper collage story")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=int, default=360, help="duration in frames")
    args = parser.parse_args()

    root = args.output_dir.resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"Refusing to write into non-empty directory: {root}")

    root.mkdir(parents=True, exist_ok=True)
    for subdir in [
        "src",
        "public/assets/backgrounds",
        "public/assets/layers",
        "public/audio",
        "scripts",
        "out",
    ]:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    package = {
        "scripts": {
            "start": "remotion studio src/index.ts",
            "still": "remotion still PaperCutout out/check-frame.png --frame=90 --scale=0.5",
            "render": "remotion render src/index.ts PaperCutout out/final.mp4",
            "audit-assets": "python3 scripts/audit_assets.py",
            "check": "bash scripts/check_render.sh out/final.mp4",
        },
        "dependencies": {
            "@remotion/cli": "latest",
            "@remotion/media": "latest",
            "@remotion/renderer": "latest",
            "remotion": "latest",
            "react": "latest",
            "react-dom": "latest",
        },
        "devDependencies": {
            "@types/react": "latest",
            "@types/react-dom": "latest",
            "typescript": "^5.8.3",
        },
    }
    write(root / "package.json", json.dumps(package, indent=2) + "\n")
    write(root / "tsconfig.json", """{
      "compilerOptions": {
        "target": "ES2022",
        "module": "ESNext",
        "jsx": "react-jsx",
        "moduleResolution": "Bundler",
        "strict": true,
        "noEmit": true,
        "skipLibCheck": true,
        "esModuleInterop": true
      }
    }
    """)
    write(root / ".gitignore", """node_modules
out
.DS_Store
""")

    write(root / "src/index.ts", """import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';

registerRoot(RemotionRoot);
""")

    write(root / "src/Root.tsx", f"""import {{Composition}} from 'remotion';
import {{PaperCutoutVideo}} from './PaperCutoutVideo';
import {{scenes}} from './scenes';

export const RemotionRoot = () => {{
  return (
    <Composition
      id="PaperCutout"
      component={{PaperCutoutVideo}}
      durationInFrames={{{args.duration}}}
      fps={{{args.fps}}}
      width={{{args.width}}}
      height={{{args.height}}}
      defaultProps={{{{
        title: {json.dumps(args.title)},
        theme: {json.dumps(args.theme)},
        scenes,
      }}}}
    />
  );
}};
""")

    write(root / "src/scenes.ts", f"""export type LayerRole = 'primary' | 'secondary' | 'tertiary' | 'rear' | 'foreground' | 'decor';

export type LayerSpec = {{
  src: string;
  role: LayerRole;
  x: number;
  y: number;
  width: number;
  zIndex: number;
  delay: number;
  enterFrom?: 'left' | 'right' | 'bottom' | 'top';
  float?: number;
  rotate?: number;
}};

export type SceneSpec = {{
  id: string;
  from: number;
  duration: number;
  background: string;
  narration: string;
  subtitle: string;
  layers: LayerSpec[];
}};

export const scenes: SceneSpec[] = [
  {{
    id: 'opening',
    from: 0,
    duration: 180,
    background: 'assets/backgrounds/opening.svg',
    narration: 'Introduce {args.theme}.',
    subtitle: {json.dumps(args.title)},
    layers: [
      {{src: 'assets/layers/rear-hills.svg', role: 'rear', x: 150, y: 360, width: 560, zIndex: 1, delay: 4, enterFrom: 'left', float: 8}},
      {{src: 'assets/layers/primary-subject.svg', role: 'primary', x: 670, y: 210, width: 610, zIndex: 3, delay: 16, enterFrom: 'bottom', float: 16, rotate: -2}},
      {{src: 'assets/layers/secondary-subject.svg', role: 'secondary', x: 1180, y: 370, width: 380, zIndex: 2, delay: 32, enterFrom: 'right', float: 10, rotate: 2}},
      {{src: 'assets/layers/foreground-paper.svg', role: 'foreground', x: 0, y: 760, width: 1920, zIndex: 5, delay: 0, enterFrom: 'bottom', float: 5}},
    ],
  }},
  {{
    id: 'close',
    from: 180,
    duration: 180,
    background: 'assets/backgrounds/close.svg',
    narration: 'Reveal the main idea with layered paper depth.',
    subtitle: 'Layer the scene, stagger the entrances, then let narration drive the edit.',
    layers: [
      {{src: 'assets/layers/tertiary-note.svg', role: 'tertiary', x: 310, y: 270, width: 360, zIndex: 1, delay: 8, enterFrom: 'left', float: 9, rotate: -4}},
      {{src: 'assets/layers/primary-subject.svg', role: 'primary', x: 790, y: 170, width: 520, zIndex: 3, delay: 18, enterFrom: 'bottom', float: 15, rotate: 1}},
      {{src: 'assets/layers/foreground-paper.svg', role: 'foreground', x: 0, y: 760, width: 1920, zIndex: 5, delay: 0, enterFrom: 'bottom', float: 6}},
    ],
  }},
];
""")

    write(root / "src/PaperCutoutVideo.tsx", """import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Audio} from '@remotion/media';
import type {LayerSpec, SceneSpec} from './scenes';

type Props = {
  title: string;
  theme: string;
  scenes: SceneSpec[];
};

const roleMotion = {
  primary: {distance: 78, rise: 55, startScale: 0.86},
  secondary: {distance: 58, rise: 38, startScale: 0.9},
  tertiary: {distance: 38, rise: 22, startScale: 0.95},
  rear: {distance: 28, rise: 16, startScale: 0.96},
  foreground: {distance: 46, rise: 26, startScale: 0.96},
  decor: {distance: 28, rise: 18, startScale: 0.96},
} as const;

const enterOffset = (layer: LayerSpec, amount: number) => {
  switch (layer.enterFrom ?? 'bottom') {
    case 'left':
      return `${-amount}px 0px`;
    case 'right':
      return `${amount}px 0px`;
    case 'top':
      return `0px ${-amount}px`;
    case 'bottom':
    default:
      return `0px ${amount}px`;
  }
};

const PaperLayer: React.FC<{layer: LayerSpec; sceneFrame: number}> = ({layer, sceneFrame}) => {
  const motion = roleMotion[layer.role];
  const local = Math.max(0, sceneFrame - layer.delay);
  const entrance = interpolate(local, [0, 26], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const drift = Math.sin((sceneFrame + layer.delay) / 28) * (layer.float ?? 6);

  return (
    <Img
      src={staticFile(layer.src)}
      style={{
        position: 'absolute',
        left: layer.x,
        top: layer.y,
        width: layer.width,
        zIndex: layer.zIndex,
        opacity: entrance,
        translate: interpolate(entrance, [0, 1], [enterOffset(layer, motion.distance), `0px ${-drift}px`]),
        scale: interpolate(entrance, [0, 1], [motion.startScale, 1]),
        rotate: `${(layer.rotate ?? 0) + interpolate(entrance, [0, 1], [-3, 0])}deg`,
        filter: 'drop-shadow(0 10px 0 rgba(255,255,255,.92)) drop-shadow(0 22px 22px rgba(50,35,20,.26))',
      }}
    />
  );
};

const Scene: React.FC<{scene: SceneSpec}> = ({scene}) => {
  const frame = useCurrentFrame();
  const sceneFrame = frame - scene.from;
  const bgScale = interpolate(sceneFrame, [0, scene.duration], [1, 1.018], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const subtitleOpacity = interpolate(sceneFrame, [14, 32, scene.duration - 24, scene.duration - 8], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#efe2c8', overflow: 'hidden'}}>
      <Img
        src={staticFile(scene.background)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          scale: bgScale,
        }}
      />
      {scene.layers.map((layer) => (
        <PaperLayer key={`${scene.id}-${layer.src}-${layer.zIndex}`} layer={layer} sceneFrame={sceneFrame} />
      ))}
      <div
        style={{
          position: 'absolute',
          left: 120,
          right: 120,
          bottom: 72,
          zIndex: 20,
          opacity: subtitleOpacity,
          color: '#251d16',
          fontFamily: 'Georgia, "Times New Roman", serif',
          fontSize: 48,
          lineHeight: 1.18,
          textAlign: 'center',
          textShadow: '0 2px 0 rgba(255,255,255,.8)',
          background: 'rgba(255, 248, 230, .72)',
          borderRadius: 0,
          padding: '20px 30px',
        }}
      >
        {scene.subtitle}
      </div>
    </AbsoluteFill>
  );
};

export const PaperCutoutVideo: React.FC<Props> = ({scenes}) => {
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill>
      {scenes.map((scene) => (
        <Sequence key={scene.id} from={scene.from} durationInFrames={scene.duration}>
          <Scene scene={scene} />
        </Sequence>
      ))}
      <Sequence durationInFrames={durationInFrames}>
        <Audio src={staticFile('audio/narration.wav')} volume={1} />
      </Sequence>
    </AbsoluteFill>
  );
};
""")

    write(root / "QUALITY_GATES.md", f"""# Quality Gates

This project was generated with draft placeholder SVG assets and silent placeholder audio.

Before calling any render final:

- record the requested canvas: `{args.width}x{args.height}` at `{args.fps}` fps;
- write a reference/style brief if references were supplied;
- replace default placeholder characters with high-quality transparent PNG/WebP cutouts;
- create a consistent hero character pack for named protagonists;
- replace placeholder narration with authorized final narration;
- verify subtitles against the narration transcript;
- run `npm run audit-assets`, `npm run still`, `npm run render`, and `npm run check`.

If `npm run audit-assets` fails, the video is still a draft.
""")

    write(root / "scripts/check_render.sh", """#!/usr/bin/env bash
set -euo pipefail

VIDEO="${1:-out/final.mp4}"
python3 scripts/audit_assets.py

if [[ ! -f "$VIDEO" ]]; then
  echo "Missing render: $VIDEO" >&2
  exit 2
fi

ffprobe -v error -show_streams -show_format "$VIDEO"
ffmpeg -y -ss 1 -i "$VIDEO" -frames:v 1 out/check-01.png >/dev/null 2>&1
ffmpeg -y -i "$VIDEO" -vf "fps=1/4,scale=360:-1,tile=5x3:margin=8:padding=4:color=white" -frames:v 1 out/contact-sheet.jpg >/dev/null 2>&1 || true
echo "Wrote out/check-01.png"
[[ -f out/contact-sheet.jpg ]] && echo "Wrote out/contact-sheet.jpg"
""", executable=True)

    write(root / "scripts/audit_assets.py", """#!/usr/bin/env python3
\"\"\"Block final delivery while draft placeholders remain.\"\"\"

from __future__ import annotations

from pathlib import Path
import sys
import wave


ROOT = Path(__file__).resolve().parents[1]
DRAFT_SVGS = {
    "primary-subject.svg",
    "secondary-subject.svg",
    "rear-hills.svg",
    "tertiary-note.svg",
    "foreground-paper.svg",
    "opening.svg",
    "close.svg",
}


def has_non_silent_audio(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with wave.open(str(path), "rb") as wav:
            frames = wav.readframes(min(wav.getnframes(), wav.getframerate() * 3))
    except wave.Error:
        return True
    return any(byte != 0 for byte in frames)


def main() -> int:
    issues: list[str] = []
    assets = ROOT / "public" / "assets"
    remaining = [p.name for p in assets.rglob("*.svg") if p.name in DRAFT_SVGS]
    if remaining:
        issues.append(
            "draft SVG placeholders remain: " + ", ".join(sorted(remaining))
        )

    layer_dir = assets / "layers"
    final_cutouts = [
        p for p in layer_dir.rglob("*")
        if p.suffix.lower() in {".png", ".webp"} and "placeholder" not in p.name.lower()
    ]
    if len(final_cutouts) < 4:
        issues.append("fewer than 4 final PNG/WebP cutout layers found")

    narration = ROOT / "public" / "audio" / "narration.wav"
    if not has_non_silent_audio(narration):
        issues.append("narration.wav is missing or silent placeholder audio")

    if issues:
        print("Asset audit failed; this render is still DRAFT:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("Asset audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""", executable=True)

    write(root / "scripts/generate_voice.sh", """#!/usr/bin/env bash
set -euo pipefail

REF_AUDIO="${1:?reference audio path required}"
REF_TEXT="${2:?reference transcript required}"
GEN_TEXT="${3:?generation text required}"
OUT="${4:-public/audio/narration.wav}"

f5-tts_infer-cli \\
  --ref_audio "$REF_AUDIO" \\
  --ref_text "$REF_TEXT" \\
  --gen_text "$GEN_TEXT" \\
  --output_dir "$(dirname "$OUT")" \\
  --output_file "$(basename "$OUT")" \\
  --device mps
""", executable=True)

    write(root / "scripts/split_sheet.py", '''#!/usr/bin/env python3
"""Split a horizontal sprite sheet into transparent PNG layers.

Usage:
  python scripts/split_sheet.py sheet.png public/assets/layers hero 6
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def trim_alpha(img: Image.Image) -> Image.Image:
    alpha = np.array(img.getchannel("A"))
    ys, xs = np.where(alpha > 10)
    if len(xs) == 0 or len(ys) == 0:
        return img
    return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def make_green_transparent(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.array(rgba)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mask = (g > 120) & (g > r * 1.25) & (g > b * 1.25)
    arr[:, :, 3] = np.where(mask, 0, arr[:, :, 3])
    return Image.fromarray(arr)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sheet", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("prefix")
    parser.add_argument("count", type=int)
    parser.add_argument("--green-key", action="store_true")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(args.sheet).convert("RGBA")
    if args.green_key:
        img = make_green_transparent(img)

    cell_w = img.width // args.count
    for index in range(args.count):
        cell = img.crop((index * cell_w, 0, (index + 1) * cell_w, img.height))
        layer = trim_alpha(cell)
        out = args.out_dir / f"{args.prefix}-{index + 1:02d}.png"
        layer.save(out)
        print(out)


if __name__ == "__main__":
    main()
''', executable=True)

    write(root / "public/assets/backgrounds/opening.svg", svg(1920, 1080, """
  <path d="M0 680 C300 590 520 640 790 560 C1080 470 1420 560 1920 430 L1920 1080 L0 1080 Z" fill="#d7b56d"/>
  <path d="M0 760 C420 640 780 760 1100 650 C1390 550 1650 610 1920 520 L1920 1080 L0 1080 Z" fill="#b78553"/>
  <circle cx="1500" cy="220" r="115" fill="#e3844d"/>
  <rect x="760" y="330" width="390" height="360" rx="18" fill="#a14335"/>
  <polygon points="690,345 955,190 1220,345" fill="#7a302b"/>
"""))
    write(root / "public/assets/backgrounds/close.svg", svg(1920, 1080, """
  <rect x="0" y="0" width="1920" height="1080" fill="#edd7ae"/>
  <path d="M0 780 C260 670 540 720 760 630 C1040 520 1390 580 1920 470 L1920 1080 L0 1080 Z" fill="#c49d63"/>
  <rect x="520" y="220" width="880" height="520" rx="20" fill="#f2e2bd"/>
  <path d="M540 250 L1370 205 L1415 730 L500 755 Z" fill="#fff4d5" opacity=".65"/>
"""))
    write(root / "public/assets/layers/rear-hills.svg", svg(900, 420, """
  <path d="M20 350 C180 110 270 220 390 80 C530 230 690 60 875 350 Z" fill="#789167"/>
  <path d="M70 370 C230 210 360 290 480 190 C620 310 730 170 850 370 Z" fill="#5c7658"/>
"""))
    write(root / "public/assets/layers/primary-subject.svg", svg(760, 760, """
  <ellipse cx="382" cy="665" rx="210" ry="44" fill="#000" opacity=".14"/>
  <circle cx="380" cy="210" r="115" fill="#d99656"/>
  <path d="M250 340 C310 280 455 280 515 340 L585 650 L175 650 Z" fill="#bc4f3f"/>
  <path d="M235 390 L525 315 L570 430 L275 510 Z" fill="#f6d17a"/>
  <circle cx="338" cy="200" r="13" fill="#3a2520"/>
  <circle cx="420" cy="200" r="13" fill="#3a2520"/>
"""))
    write(root / "public/assets/layers/secondary-subject.svg", svg(520, 620, """
  <ellipse cx="260" cy="550" rx="150" ry="35" fill="#000" opacity=".12"/>
  <circle cx="260" cy="160" r="82" fill="#d49a66"/>
  <path d="M150 260 C210 220 315 220 370 260 L420 545 L100 545 Z" fill="#3f7291"/>
  <path d="M125 340 L390 300 L410 390 L145 430 Z" fill="#e9c46a"/>
"""))
    write(root / "public/assets/layers/tertiary-note.svg", svg(500, 360, """
  <path d="M70 70 L430 42 L456 290 L42 315 Z" fill="#fff2cf"/>
  <path d="M115 130 L380 110" stroke="#9b6b48" stroke-width="18" stroke-linecap="round"/>
  <path d="M105 190 L350 176" stroke="#9b6b48" stroke-width="14" stroke-linecap="round"/>
  <path d="M120 245 L310 235" stroke="#9b6b48" stroke-width="12" stroke-linecap="round"/>
"""))
    write(root / "public/assets/layers/foreground-paper.svg", svg(1920, 360, """
  <path d="M0 160 C250 110 480 190 720 145 C980 92 1190 190 1450 130 C1650 82 1790 130 1920 100 L1920 360 L0 360 Z" fill="#f7e8bf"/>
  <path d="M0 235 C370 175 590 260 930 210 C1280 155 1570 230 1920 172 L1920 360 L0 360 Z" fill="#ead09b"/>
"""))

    write(root / "public/audio/README.txt", """Place narration.wav, BGM, and SFX here.
The template references public/audio/narration.wav. Generate or import that file before final render.
""")
    write_silence(root / "public/audio/narration.wav", args.duration / args.fps)

    print(root)


if __name__ == "__main__":
    main()
