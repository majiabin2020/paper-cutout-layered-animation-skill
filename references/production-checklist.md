# Production Checklist

## Environment

- `node --version` works.
- `ffmpeg -version` and `ffprobe -version` work.
- F5-TTS venv activates and `f5-tts_infer-cli --help` works when final voice generation is required.
- If offline or slow, run `scripts/prefetch_f5tts.py` once while network is available.

## Reference and format

- User-requested canvas is recorded: width, height, fps, duration.
- Reference videos/images are inspected when supplied.
- Reference style brief is written: paper texture, outline/rim, palette, subtitle style, character detail, scene density, motion cadence.
- Aspect ratio is not blindly copied from references unless the user asked to match it.

## Story

- The topic is reduced to timed beats.
- Every beat has one focal subject, one visual action, one narration segment, and exact subtitle cue.
- The first beat establishes the visual world; the last beat resolves or lands the point.
- Narration and subtitles use the same source transcript.

## Character and assets

- Named protagonist has a consistent character pack before scene production.
- No final scene uses geometric placeholder people, emoji figures, or generic silhouettes as the main character.
- Background plates have no text and no main characters.
- Character/object layers are transparent PNG/WebP when possible.
- Each scene has at least one primary cutout, supporting layers, and foreground/depth treatment.
- Filenames are stable and match `src/scenes.ts`.
- Scaffold SVGs are removed or explicitly classified as draft-only ornaments.

## Remotion

- Assets live under `public/` and are loaded with `staticFile()`.
- Animations use `useCurrentFrame()` with `interpolate()` or `Easing`.
- No CSS `animation` or `transition`.
- Scene specs live in `src/scenes.ts`.
- Subtitles stay inside safe margins and remain readable at preview size.
- Contact sheet shows clear focal hierarchy in representative frames.

## Subtitles

- Every narration segment has a matching subtitle cue.
- Chinese text is visually inspected in rendered frames.
- Subtitle style matches the brief/reference: contrast, position, font, box/background, line length.
- No wrong characters, missing cues, or impossible reading speed.

## Audio

- Voice reference audio is authorized.
- Celebrity/person-specific cloning is not used without explicit rights.
- Placeholder/system TTS is labeled draft, never final.
- Final narration is listened to for human-likeness, pronunciation, pacing, clipping, noise, and sync.
- BGM/SFX are quieter than voice and do not mask consonants.

## Verification

- Run `npm run audit-assets` if available.
- Run `npm run still` and inspect the still.
- Render a contact sheet and compare against the style brief/reference frames.
- Run `npm run render`.
- Run `npm run check` and confirm ffprobe sees video/audio streams.
- Watch the final MP4 once with sound and once muted.
- Final claim is blocked if any item above fails.
