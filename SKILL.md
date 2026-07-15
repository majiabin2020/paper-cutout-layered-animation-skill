---
name: 纸片分层动画生成Skill
description: 用于制作纸片分层动画视频，包括分镜策划、素材分层、透明抠图、Remotion 动画、旁白配音、字幕同步、音视频质检和可复用主题生成流程。
---

# 纸片分层动画生成Skill

Current workflow level: **V4.8 voice-palette quality gate**.

## Non-negotiable principle

Do not ship a “working render” as a finished paper-cutout video. A render is final only after it passes reference alignment, asset quality, subtitle, audio, and MP4 verification gates.

The output format follows the user request. If the user wants horizontal, make horizontal. If vertical, make vertical. Reference videos define quality and style targets, not mandatory aspect ratio.

V4.4 lesson: the final result is judged by perceived video quality, not by whether the pipeline technically rendered. The main failure modes are ugly or inconsistent characters, dirty cutout edges, static layered images, robotic voice, mistimed subtitles, and unverified residue in transparent PNGs.

V4.5 lesson: reference-quality paper animation is a repeatable visual system, not a pile of independent illustrations. Before asset generation, define the mode, style bible, protagonist pack, layer manifest, motion grammar, and scoring rubric. If those are missing, the result will drift even when every individual asset looks acceptable.

V4.6 lesson: do not rely on taste notes alone. Convert repeatable checks into small portable tools, and convert visual variety into reusable template families. A skill should tell future agents both what to judge and what scripts/templates to create when the local project lacks them.

V4.7 lesson: the asset art layer is a system, not decoration. A reusable workflow must define paper texture, rim behavior, shadow depth, topic-specific prop vocabulary, and layer density. Geometric placeholder people, flat SVG-like props, clean rectangular cards, or identical white rims make the result feel cheap even if motion and QA pass.

V4.8 lesson: narration is a casting decision. A reusable workflow cannot ship with only one default voice, one gender, or one age profile. The voice palette must cover multiple genders, ages, tones, and content categories, and the chosen voice must match the video type rather than being whatever the local TTS script happened to use first.

## Start here

1. If first-time setup is needed, run `scripts/install_env.sh`. Do not reinstall when the user says dependencies are already installed.
2. If reference videos/images are provided, inspect them before storyboarding:
   - `ffprobe` for duration/fps/size/audio.
   - contact sheet or representative frames for style, composition, subtitle treatment, character detail, paper texture, motion density.
3. Decide canvas from user intent, not from references unless the user asks to match them. Common presets:
   - horizontal: `1920x1080`
   - vertical short video: `1080x1920` or user-specified
   - reference-like tall card: `1080x1440`
4. Create a project with `scripts/create_project.py <output-dir> --title "..." --theme "..." --width ... --height ... --duration ...`.
5. Treat generated scaffold assets as draft placeholders only. Replace them with real generated or user-provided layered assets before final render.
6. Choose the production mode before generating assets:
   - `archival-card`: reference-like historical paper card, fixed title/subtitle system, old-paper canvas, maps, labels, props, army/group cutouts, strong layout consistency.
   - `cinematic-cutout`: wider filmic scenes, stronger atmosphere, camera depth, character closeups, more scene-to-scene visual variation.
   - `explainer-board`: education/science/business explainer, diagrams, labels, icons, flow arrows, charts, object callouts.
   - `lifestyle-craft`: food/life/travel/entertainment, warm tabletop paper props, packaging, utensils, stickers, playful micro-motion.
7. Choose a narration voice profile before voice generation. Define gender, approximate age band, delivery style, speed, emotional intensity, and use case. Do not hard-code one default narrator across all topics.
8. If project helper tools are missing, create or install portable tools before final QA. Prefer Python + FFmpeg + Pillow/OpenCV + NumPy + Remotion scripts that most agents can reproduce.
9. Track versions by delivery quality, not render count. A version bump should name what changed, such as `v4.8-voice-palette`, `v4.7-asset-art`, `v4.6-template-audit`, `v4.5-archival-card-system`, `v4.4-cleaned-cutout-residue`, `v4.3-neural-commercial-narration`, or `rich-motion`.

## Quality workflow

Use this order.

1. **Reference alignment**
   - Write a short style brief: canvas, palette, paper texture, edge treatment, character scale, subtitle style, scene density, motion cadence, audio tone.
   - If no reference is provided, create the brief from the user’s topic and desired platform.
   - V4.5 requires a style bible before generating final assets. Include:
     - production mode: `archival-card` or `cinematic-cutout`;
     - canvas and safe area;
     - paper base color, texture strength, age stains, and torn-corner vocabulary;
     - cutout rim thickness, shadow direction, and shadow softness;
     - protagonist scale range and camera distance;
     - title tag, subtitle box, font feel, line length, and margins;
     - palette and contrast rules;
     - motion grammar: allowed entry, exit, idle, and transition moves;
     - recurring props and visual motifs.
   - Reference videos define the target visual system: repeated layout, repeated typography, repeated paper texture, repeated character proportions, and repeated prop grammar. Do not imitate only the surface “paper cutout” look.

2. **Story and timing**
   - Build 4-8 beats for a 30-90s video unless user requests otherwise.
   - Each beat has one focal subject, one visual action, one narration segment, and exact subtitle text.
   - Narration and subtitles must share the same source text; never invent separate unverified subtitles.
   - Each beat must name the narrative device, not only the location. Good devices: map reveal, letter, army formation, shoe/weapon/token, tent/court conversation, route line, portrait card, before/after contrast, rumor label.
   - For `archival-card`, prefer compact historical beats with one clear “paper card” idea per scene. Avoid purely atmospheric scenic shots that do not advance the explanation.

3. **Hero character pack**
   - Before scene production, create or import a consistent protagonist pack: front/three-quarter/back or action variants, same face/clothes/palette.
   - For stories with named people, the protagonist must be recognizable inside every scene where they matter.
   - Do not use geometric SVG people, emoji-like figures, or generic silhouettes for final output.
   - For historical or cinematic stories, use protagonist closeups and action poses with stable costume, hair, face direction, and paper outline. A scene where the story depends on a named person but the person is absent, tiny, or generic fails.
   - V4.5 protagonist pack minimum:
     - portrait/closeup;
     - standing full body;
     - side or three-quarter view;
     - back view or walking pose;
     - action pose tied to the story;
     - small-scale icon/card variant if the video uses maps or diagrams.
   - Reuse the pack across scenes. Regenerate only if the whole pack fails. Do not create a new face/costume per scene.
   - For ensemble stories, define primary, secondary, and crowd packs separately. Crowd packs must not visually compete with the protagonist.

4. **Scene asset pack**
   - For every scene, require:
     - one background plate with no burned-in text;
     - one primary transparent PNG cutout;
     - supporting transparent PNG cutouts for secondary/rear/foreground/decor layers;
     - intentional foreground occlusion or depth layer.
   - Prefer transparent PNG/WebP. SVG is allowed only for simple ornaments or draft blocking, not final characters.
   - Cutouts must be visually inspected on a checkerboard before use. Reject or clean:
     - accidental source-image leftovers, such as boat, building, body, text, or frame fragments;
     - white/black rectangular alpha residue;
     - unintentional semi-transparent blocks;
     - dirty halos that are not the intended torn-paper rim;
     - unrelated objects inside smoke, petals, curtains, characters, or foreground pieces.
   - Keep `cutouts_original/` backups before alpha cleanup. Save the cleaned asset into `cutouts/`.
   - For suspicious assets, render a diagnostic contact sheet on checkerboard with alpha bbox labels. Do not rely on the final composition to reveal defects.
   - Avoid extracting all layers from one completed illustration. Generate or prepare independent transparent assets for characters, props, smoke, flags, curtains, map scraps, labels, and foreground paper pieces whenever possible.
   - Each scene must have a `Layer Manifest` before implementation:
     - background plate;
     - rear atmosphere/depth;
     - mid prop or narrative object;
     - protagonist or focal group;
     - secondary figure/group if needed;
     - foreground occluder;
     - floating particles/small paper pieces;
     - title/subtitle layers.
   - If a scene lacks either a focal character/group or a focal prop/device, it is probably just a wallpaper and should be redesigned.
   - For `archival-card`, require recurring card elements: old-paper base, torn corners, small title label, map/diagram/prop layer, protagonist/crowd cutouts, bottom subtitle box.
   - V4.7 asset-art requirements:
     - paper pieces need visible fiber/grain, mild stains, non-uniform color, and slightly irregular torn edges;
     - white paper rims should vary in thickness and contour; avoid perfectly even sticker borders unless that is the chosen design system;
     - each important paper piece should have believable depth: soft cast shadow, contact shadow, and role-based visual weight;
     - topic templates must include real prop vocabulary, not generic icons. War needs terrain/maps/flags/formations/smoke/seals; business needs product cards/users/charts/contracts/notes/arrows; food needs bowls/steam/ingredients/menus/tableware/table texture;
     - generated asset packs must include at least background base, main card, primary subject, 2-4 mid props, 1-2 foreground/occlusion pieces, and atmosphere/particle layers;
     - if the protagonist or subject is still a simple geometric symbol, label the result draft unless the user explicitly requested a flat icon style.

5. **Remotion implementation**
   - Keep scene specs data-driven in `src/scenes.ts`.
   - Use `<Img>`, `staticFile()`, `Sequence`, `useCurrentFrame()`, `interpolate()`, and `Easing`.
   - Use measured motion: paper-card entrance, slight parallax, subtle drift, occasional camera push. Avoid random clutter.
   - Preserve a clear focal hierarchy: background → rear → secondary → primary → foreground → subtitle.
   - Do not make a video that is effectively a still image. Each scene needs motion across multiple layer classes:
     - background/camera: slow push, pan, or parallax;
     - primary characters: hinge, bob, breathe, pop, or puppet-like rotation;
     - foreground: curtain swing, petal flutter, ember drift, mist slide, paper-bit fall;
     - transitions: at least some layers must enter/exit with non-fade motion.
   - Avoid fade-only entry/exit. Mix `flipLeft`, `flipRight`, `drop`, `pop`, `slideLeft`, `slideRight`, `floatUp`, `fall`, `shrink`, and `spinOut` as appropriate. Motion should feel like physical paper pieces, not slideshow opacity.
   - Keep motion intentional. More movement is not automatically better: the protagonist and story beat remain the focal point.
   - V4.5 motion grammar:
     - large paper pieces move slower than small pieces;
     - pivots should use believable paper anchors: bottom edge, top pin, corner, center only when appropriate;
     - entry motion should include slight overshoot or settle;
     - idle motion should be low amplitude but visible;
     - foreground moves more than background;
     - route lines, map markers, flags, smoke, petals, embers, and small labels should have independent micro-motion.
   - Motion density gate: sample the final video every 2-4 seconds. If a scene has no meaningful layer/camera/prop change for more than 3 seconds, it fails unless it is an intentional pause.
   - Each 10 seconds should contain at least one visible story change: prop appears, map moves, label changes, formation enters, character changes pose, foreground wipes, or camera reframes.
   - Do not confuse random movement with animation quality. Motion should explain the story or sell paper materiality.

6. **Subtitles**
   - Use the exact narration transcript split into readable subtitle cues.
   - Style to match the project brief. Common reference style: bottom black translucent box, white Chinese text, high contrast, safe margins.
   - Render stills containing every subtitle cue or enough frames to cover all cues; inspect Chinese correctness visually. If OCR is available, use it, but visual inspection is still required.
   - Subtitle timing must be generated from final audio, not from draft text estimates. If audio is stretched, compressed, regenerated, or re-cut, rewrite the cue timings.
   - If subtitles visibly lead or lag narration, the render fails even if the MP4 is technically valid.
   - V4.5 subtitle/title system:
     - fixed bottom box style across the video;
     - fixed safe margins and max line length;
     - readable contrast over every background;
     - no overlap with protagonist face or primary prop;
     - small top-left scene label/title if matching archival-card references.
   - Subtitles are part of the design system, not an afterthought overlay.

7. **Voice and audio**
   - F5-TTS may only use authorized reference audio and transcript. Never clone a real person’s voice without permission; for celebrity-like requests, use a non-identifying style description instead.
   - Mac system TTS or placeholder narration is draft only.
   - Final audio must be listened to for human-likeness, pronunciation, pacing, clipping, noise, and sync. Bad voice quality blocks final delivery.
   - Mix BGM/SFX after narration timing; voice must remain clearly dominant.
   - Do not present macOS `say` voices as final for commercial, historical, documentary, or advertisement-style narration. They are draft placeholders and often sound robotic.
   - If no authorized human reference audio is provided, use a non-identifying neural TTS voice appropriate to the brief, such as Chinese news/documentary/commercial narration. State clearly that it is not cloning a specific real person.
   - V4.8 requires a voice casting decision before generating final narration:
     - gender/profile: male, female, neutral, ensemble, or user-provided authorized reference;
     - age band: child, teen, young adult, mature adult, senior;
     - delivery style: documentary, commercial, storyteller, education/teacher, warm lifestyle, energetic entertainment, calm news, dramatic trailer;
     - emotion range: restrained, warm, curious, urgent, humorous, solemn, inspirational;
     - pacing: slow, normal, brisk, or highly rhythmic.
   - Do not use one voice for every video category. The same topic-to-video skill must support a configurable voice palette.
   - If the user does not specify a voice, infer one from topic and audience, then record it in the project config or style brief.
   - Generate or select voice through a project-level configuration such as `voice_profile.json`, `voice_profiles.ts`, or script arguments. Avoid hard-coded speaker IDs, hard-coded sample files, or one fixed provider voice inside `generate_voice.py`.
   - Avoid large global time-stretching of narration. If the script is too short or too long, revise the narration text first. Heavy `atempo` or extreme speed changes make the voice sound electronic.
   - Prefer natural script length: for a 60s video, target narration around 55-60s with small silence or mild tempo only.
   - Label voice quality honestly:
     - `draft`: system TTS or rough local placeholder;
     - `acceptable`: non-identifying neural TTS with suitable style and clean sync;
     - `premium`: authorized reference voice cloning or recorded human narration.
   - Commercial/history/documentary tone should be calm, controlled, and lightly emotional. Overacted theatrical delivery fails even if it is expressive.

   Recommended Chinese narration palette:

   | Video type | Default voice profile | Avoid |
   |---|---|---|
   | History / biography / documentary | mature adult male or female, calm documentary, medium-low intensity, normal pace | comedy delivery, overacted trailer voice, robotic monotone |
   | War / strategy / suspense | mature adult male or female, solemn/urgent but controlled, slightly slower pace | shouting, excessive drama, game-announcer exaggeration |
   | Business / product / commercial | young or mature adult male/female, clean commercial, confident, brisk but not rushed | hard sales voice, fake enthusiasm, stiff newsreader |
   | Education / science / explainer | young or mature adult male/female, teacher-like, clear articulation, warm curiosity | flat textbook reading, childish over-bright tone |
   | Lifestyle / food / travel | young adult or mature adult female/male, warm, close, relaxed, slightly smiling | official broadcast tone, cold documentary style |
   | Entertainment / gossip / social media | young adult male/female, lively, playful, rhythmic | deadpan corporate voice unless ironic |
   | Children / family | young adult or mature adult, gentle and bright; child voice only when appropriate and high-quality | synthetic child voice that sounds uncanny |
   | Myth / folktale / story | mature adult storyteller, warm dramatic arc, moderate emotion | news tone, commercial hard sell |

   Minimum voice palette for a shareable skill:

   - `female_young_warm_lifestyle`
   - `female_mature_documentary`
   - `male_young_commercial`
   - `male_mature_history`
   - `neutral_teacher_explainer`
   - `energetic_entertainment`
   - `male_dramatic_story`
   - `female_young_clean_explainer`
   - `female_news_documentary`
   - `child_or_teen_bright_education`
   - `regional_folk_story`
   - `soft_storyteller`
   - `news_public_information`
   - `warm_family_parental`
   - optional premium slots for authorized cloned/reference voices.

   For Chinese projects, a stronger shareable palette should include at least 12 configured profiles. Standard Mandarin should be the default for broad distribution; regional accents such as Northeast Mandarin, Shaanxi/Zhongyuan Mandarin, Taiwan Mandarin, Hong Kong Chinese, or Cantonese should be opt-in and only used when the topic/audience fits.

   Voice acceptance checklist:

   - pronunciation is correct, especially names and historical terms;
   - breath, pause, and sentence stress sound intentional;
   - the tone matches the content category and visual style;
   - it does not sound like a single generic assistant reading every topic;
   - subtitles are regenerated from the final audio timing after any voice change;
   - if three or more video categories are generated as examples, at least two distinct gender/age/tone profiles must be used.

8. **Verification gate**
   - Render representative stills/contact sheet.
   - Compare the sheet against the style brief/reference frames.
   - Run render and ffprobe checks.
   - Watch the final MP4 once with sound and once muted.
   - Do not claim completion if any gate fails.
   - When the user reports a visual defect, locate the exact scene, layer, and frame. Render a still at that frame after the fix before re-rendering the full MP4.
   - For alpha/cutout defects, inspect the source PNG on checkerboard and compare cleaned vs original. The root cause must be identified before cleanup.
   - Full delivery requires a new MP4 after the fix, not only a corrected source asset.
   - V4.5 also requires a reference-system comparison sheet:
     - contact sheet for reference video(s);
     - contact sheet for produced video;
     - written comparison on layout consistency, protagonist consistency, prop/story devices, paper texture, motion density, subtitle system, and audio tone.
   - Score the final video before delivery. Any score below 3/5 in protagonist consistency, cutout cleanliness, subtitle sync, or voice naturalness blocks final delivery.
   - V4.6 requires automated checks whenever feasible. If a check is subjective, automate its evidence gathering and then judge visually.
   - Ending rhythm gate: the final 3 seconds must have an intentional audio and visual purpose. Verify that video duration, narration/audio duration, final subtitle cue, and final visual event align. If narration ends more than 1 second before the video without planned music/outro, or if no meaningful layer/camera/prop change occurs in the final 3 seconds, the video fails.

## V4.6 portable automation tools

These tools should be created inside each project when absent. Keep them small, scriptable, and provider-agnostic. Preferred stack: `ffmpeg/ffprobe`, Python 3, Pillow, OpenCV (`opencv-python`), NumPy, imageio, and Remotion CLI. If a dependency is missing, install it locally or write the simplest fallback.

| Tool | Purpose | Typical implementation |
|---|---|---|
| `make_reference_contact_sheet.py` | Compare references and output side-by-side frame sheets. | `ffmpeg` frame extraction + Pillow grid. |
| `make_video_contact_sheet.py` | Generate produced-video sheet at fixed intervals. | `ffmpeg -vf fps=...` or Python frame sampling. |
| `audit_cutout_alpha.py` | Detect dirty transparent PNGs: big bbox, stray islands, rectangular residue, suspicious semi-transparent blocks. | Pillow alpha channel + connected components via OpenCV/NumPy. |
| `make_cutout_checker_sheet.py` | Render all PNG/WebP cutouts on checkerboard with bbox labels. | Pillow checkerboard compositing. |
| `motion_density_check.py` | Estimate whether scenes are dead/static. | Extract frames every N frames, compute frame difference/SSIM-like delta, export CSV + sparkline/contact sheet. |
| `subtitle_sync_audit.py` | Confirm cue coverage, duration, gaps, and final cue alignment with narration length. | Parse `src/captions.ts`/JSON + `ffprobe` audio duration. |
| `audio_loudness_check.sh` | Confirm narration/BGM duration, sample rate, clipping, loudness roughness. | `ffprobe`, `ffmpeg astats`, `loudnorm` dry run. |
| `voice_palette_audit.py` | Verify project voice configuration is not a single hard-coded narrator and matches topic categories. | Parse voice profile JSON/TS + audio filenames + metadata notes. |
| `scene_manifest_lint.py` | Verify every scene has required layer roles and focal subject/prop. | Parse `src/scenes.ts` or a JSON manifest. |
| `render_issue_frame.sh` | Given seconds/frame, render a still for user-reported defects. | `npx remotion still ... --frame`. |
| `quality_scorecard.md` | Human-readable scoring evidence and pass/fail record. | Markdown template filled after automated sheets. |

Automation rule:

```text
Automate evidence; do not pretend subjective quality is fully automated.
Scripts should reveal problems early: dirty alpha, dead scenes, missing layers,
subtitle gaps, wrong duration, inconsistent contact sheets.
```

Minimum tool bundle before sharing a generated project:

```bash
python3 scripts/make_reference_contact_sheet.py --help
python3 scripts/make_cutout_checker_sheet.py --help
python3 scripts/audit_cutout_alpha.py --help
python3 scripts/motion_density_check.py --help
python3 scripts/subtitle_sync_audit.py --help
bash scripts/audio_loudness_check.sh --help
python3 scripts/voice_palette_audit.py --help
```

If `--help` is not implemented, the script should print usage when called with no args. These scripts should not require proprietary services.

## V4.6 broad template asset system

Do not ship one narrow template. Build composable template families that can cover many user topics. A template family is a style bible + Remotion layout + motion presets + prop pack + prompt pack.

Core reusable template assets:

- paper bases: old parchment, clean notebook, warm kraft, dark theater, bright lifestyle, blueprint/grid, menu/tabletop;
- torn corners and edge strips: top-left label area, side collage strips, bottom subtitle backing, foreground tears;
- title systems: archival tag, chapter stamp, sticky note, lower-third card, diagram label, menu tag;
- subtitle systems: black translucent box, parchment strip, caption card, comic balloon, clean education lower third;
- motion presets: card slide, paper flip, pin hinge, map reveal, route line draw, stamp pop, prop bounce, smoke drift, flag flutter, particle fall;
- prop primitives: map, scroll, letter, photo card, book, phone, chart, coin, product box, bowl/plate, utensils, lab bottle, plant, ticket, badge, arrow, icon sticker;
- crowd/group primitives: soldiers, office workers, students, customers, audience, family, chefs, travelers, villagers;
- atmosphere primitives: smoke, mist, petals, embers, confetti, steam, dust, rain strips, spotlight paper beams.

Template families by topic:

| User topic | Best mode | Required recurring assets |
|---|---|---|
| War / military / strategy | `archival-card` or `cinematic-cutout` | maps, route lines, flags, formations, weapons, smoke, command tent, terrain cards. |
| Historical人物 / biography | `archival-card` | protagonist pack, timeline strip, portrait card, letter/edict, map, key symbolic props. |
| Business / commercial case | `explainer-board` | product cards, growth chart, money/contract, office crowd, arrows, before/after cards. |
| Story / folktale / myth | `cinematic-cutout` | protagonist/sidekick/villain packs, magical prop, location cards, atmosphere particles. |
| Education / science / knowledge | `explainer-board` | diagrams, labels, icons, magnifier, flow arrows, formula/cards, teacher/student cutouts. |
| Life / lifestyle / travel | `lifestyle-craft` | tabletop base, stickers, map pins, luggage, phone, photo cards, weather/food props. |
| Entertainment / gossip / pop culture | `lifestyle-craft` or `explainer-board` | stage/spotlight, reaction stickers, speech bubbles, social-card frames, ranking cards. |
| Food / cooking | `lifestyle-craft` | menu paper, bowls/plates, utensils, steam, ingredient stickers, recipe steps, table texture. |
| Product ad / brand | `explainer-board` or `lifestyle-craft` | product hero, packaging, benefit icons, comparison cards, CTA card, brand-color paper set. |
| News / current affairs | `archival-card` or `explainer-board` | map, timeline, document clippings, quote cards, location labels, neutral subtitle system. |

Template selection rule:

```text
Choose a family from the user's topic and intent first. Then adapt the style
bible. Do not force every topic into historical parchment; food, product, science,
and lifestyle videos need different paper bases and prop vocabularies.
```

Each template family must define:

1. visual mood and paper base;
2. protagonist/subject treatment;
3. required props;
4. scene layout variants;
5. subtitle/title style;
6. motion presets;
7. forbidden clichés or mismatches.

## V4.7 asset-art upgrade gate

Use this when a video technically renders but still looks cheap, flat, or placeholder-like.

Minimum upgrade checklist:

- Replace flat geometric shapes with topic-specific paper illustrations.
- Add texture at three levels: canvas background, large paper cards, and individual cutouts.
- Add irregular rims and torn edges; avoid clean rectangles unless they are intentional cards.
- Add role-based shadows: rear layers subtle, primary layers stronger, foreground layers strongest.
- Expand each theme with a prop vocabulary that tells the story rather than merely decorating it.
- Inspect all cutouts on checkerboard after regeneration; intentional semi-transparent smoke/steam is acceptable, unrelated residue is not.
- Compare before/after contact sheets. The upgraded version should show richer layer density without blocking subtitles or confusing the focal subject.

## V4.8 voice-palette gate

Use this when the video pipeline has working narration but the voice still feels generic, robotic, mismatched, or monotonous across topics.

Minimum upgrade checklist:

- Define a voice palette with multiple genders, multiple age bands, and multiple delivery styles.
- For a shareable project, target at least 12 configured voice profiles, even if only 2-4 are used in one demo render.
- Select the voice profile from topic, audience, platform, and emotional intent before rendering final audio.
- Store the selected voice profile in project config or style brief.
- Use distinct voices for distinct example categories when demonstrating a reusable skill.
- Reject one-size-fits-all narration, even if the audio is technically clean.
- Regenerate subtitles and rerun sync checks after any voice change.
- Listen to the first 20 seconds and the final 20 seconds with eyes closed; if it sounds like a generic assistant, robotic announcer, or mismatched character, it is not final.

## V4.5 reference-system playbook

Use this before starting a new production or when upgrading a draft toward reference quality.

1. Extract reference facts:
   - duration, fps, canvas;
   - contact sheet;
   - recurring background texture;
   - character scale and pose repetition;
   - title/subtitle treatment;
   - prop categories;
   - motion cadence.
2. Choose mode:
   - `archival-card` for reference-like paper history explainer;
   - `cinematic-cutout` for wider dramatic story scenes.
3. Write the style bible and do not generate final assets until it exists.
4. Build protagonist and prop packs before scene generation.
5. Write a layer manifest for every scene.
6. Implement Remotion from the manifests, not from ad-hoc visual guesses.
7. Run the V4.5 quality scorecard before calling the video final.

For V4.6, insert this step between 3 and 4: choose a template family and create missing tool scripts/templates before generating final assets.

## V4.5 quality scorecard

Rate each item 0-5. Delivery requires no blocking item below 3 and an average of at least 3.8.

| Item | Blocking? | What 5/5 means |
|---|---:|---|
| Reference-system fit | Yes | The video clearly belongs to the same visual family as the reference while respecting requested aspect ratio. |
| Protagonist consistency | Yes | Same face, costume, palette, and proportions across scenes. |
| Layout/template consistency | No | Title, subtitle, paper base, margins, and focal hierarchy repeat intentionally. |
| Cutout cleanliness | Yes | No unrelated residues, dirty alpha blocks, accidental source fragments, or broken rims. |
| Paper materiality | No | Paper texture, torn edges, shadows, and depth are coherent across layers. |
| Layer richness | No | Each scene has background, depth, focal subject/prop, foreground, and particle/decor layers. |
| Motion density | No | Every scene has visible, purposeful paper motion and story changes. |
| Prop-driven storytelling | No | Maps, labels, letters, weapons, route lines, formations, or symbolic objects advance the explanation. |
| Subtitle/title system | Yes | Text is correct, synced, readable, and visually integrated. |
| Voice naturalness | Yes | Voice matches brief, is not robotic or overacted, and stays synced. |

Common reference-like targets:

- `archival-card`: fixed paper canvas, top-left label, bottom subtitle, recurring protagonist/crowd scale, map/prop overlays, restrained but constant paper motion.
- `cinematic-cutout`: deeper backgrounds, stronger atmospheric layers, protagonist closeups, foreground occlusion, richer camera parallax.
- `explainer-board`: diagrams, arrows, labels, charts, icon stickers, clear logical sequence.
- `lifestyle-craft`: warm tabletop/collage texture, playful props, ingredient/object stickers, softer color, lighter motion.

## V4.4 defect-handling playbook

Use this when the user points to a bad frame or screenshot.

1. Map the screenshot to `SceneSpec.id`, frame range, and likely layer from `src/scenes.ts`.
2. Inspect every candidate PNG/WebP on checkerboard with alpha bbox.
3. Identify whether the defect is:
   - dirty source asset;
   - bad alpha cleanup;
   - wrong layer placed in the scene;
   - background artifact;
   - motion path revealing an unwanted area.
4. Fix the root cause:
   - clean alpha if the desired cutout contains residue;
   - remove or replace the layer if the whole object is conceptually wrong;
   - regenerate the asset if cleanup would destroy the paper look.
5. Render a still at the reported frame and visually compare against the screenshot.
6. Only then render the full MP4, run `npm run check`, and copy the versioned file for delivery.

Minimal alpha-cleaning rule:

```text
Never blindly erase by color alone. Preserve the intended paper rim and texture.
Use original backups, bbox inspection, feathered masks, and frame-level stills.
```

## Project commands

From a generated project:

```bash
npm install
npm run start
npm run still
npm run render
npm run check
```

Recommended QA commands after a project has V4.6 tools:

```bash
python3 scripts/make_cutout_checker_sheet.py public/assets/cutouts out/cutouts-checker.jpg
python3 scripts/audit_cutout_alpha.py public/assets/cutouts --out out/alpha-audit.json
python3 scripts/motion_density_check.py out/final.mp4 --out out/motion-density.csv
python3 scripts/subtitle_sync_audit.py src/captions.ts public/audio/narration.wav
bash scripts/audio_loudness_check.sh out/final.mp4
npm run check
```

Generate voice after activating the F5-TTS venv:

```bash
source /path/to/.venv-f5-tts/bin/activate
./scripts/generate_voice.sh public/audio/ref.wav "reference transcript" "new narration text"
```

Generate non-identifying commercial-style neural narration when no authorized reference voice exists:

```bash
python3 scripts/generate_narration_neural.py --voice-profile female_mature_documentary
npm run render
npm run check
```

The exact script may use a local/provider neural TTS, but it must accept a voice profile argument or config, output `public/audio/narration.wav`, and regenerate `src/captions.ts` from final audio durations.

Example voice profile config:

```json
{
  "id": "female_mature_documentary",
  "language": "zh-CN",
  "gender": "female",
  "age_band": "mature_adult",
  "delivery": "documentary",
  "emotion": "calm_warm",
  "pace": "normal",
  "allowed_for": ["history", "biography", "documentary", "education"]
}
```

## Asset prompts

For a V4.5 style bible:

```text
Create a production style bible for a layered paper-cutout animation about [topic].
Mode: [archival-card or cinematic-cutout]. Define canvas, old-paper base,
torn-corner vocabulary, protagonist proportions, cutout rim thickness, shadow
direction, title/subtitle system, recurring props, color palette, and motion
grammar. The style must be repeatable across all scenes.
```

For a V4.6 template family:

```text
Design a reusable paper-cutout video template family for [topic category].
Include visual mood, paper base, protagonist/subject treatment, required prop
pack, 6 scene layout variants, subtitle/title style, motion presets, and
forbidden mismatches. It must work for multiple topics in this category, not
only one story.
```

For a V4.6 layer manifest:

```text
Create a scene-by-scene Layer Manifest for a [duration] paper-cutout video about
[topic], using the [template family] family. For each scene list background,
rear atmosphere, focal subject, focal prop/device, secondary group, foreground
occluder, particles, title, subtitle cue, and motion preset.
```

For a protagonist pack:

```text
Create a consistent paper-cutout character pack for [character]: portrait,
standing full body, side/three-quarter view, back/walking view, and one story
action pose. Same face, hair, costume, palette, white paper rim, tactile paper
fiber, soft shadow, transparent background, no text, no watermark.
```

For character cutouts:

```text
Create a high-detail handmade paper-cutout sticker of [character], [pose],
consistent face and costume, white paper rim, tactile paper fibers, soft cast
shadow, transparent background, no text, no watermark, suitable for layered
animation.
```

For background plates:

```text
Create a handmade paper-collage background plate for [scene], no main
characters, no text, layered torn-paper depth, warm paper fibers, cinematic
composition, [canvas ratio], no watermark.
```

For reference matching:

```text
Match the supplied reference quality: coherent protagonist, paper collage
texture, visible torn edges, sticker-like white outline, readable bottom
Chinese subtitles, one clear focal subject per scene. Keep the requested
canvas ratio: [width]x[height].
```

## Completion rules

- If scaffold SVGs or placeholder audio remain, call it a draft.
- If there is no style bible, protagonist pack, and scene layer manifest, call it a draft.
- If the topic was forced into the wrong template family, call it a draft.
- If missing portable QA tools were neither created nor replaced by equivalent checks, call it a draft.
- If the protagonist is missing, inconsistent, or ugly in key scenes, regenerate assets before rendering final.
- If the visual system drifts between scenes without an intentional reason, call it a draft.
- If layer motion is mostly fade-only or the video feels like a static picture, call it a draft.
- If motion does not create meaningful paper materiality or story change, call it a draft.
- If transparent PNGs contain unrelated residual objects, rectangular scraps, dirty alpha blocks, or unintended halos, fix the assets before final render.
- If subtitles are absent, mistimed, unreadable, or contain wrong Chinese, fix subtitles before rendering final.
- If voice sounds robotic or unauthorized, replace it or label it draft.
- If the project uses only one hard-coded narrator for unrelated video categories, update the voice palette and regenerate at least the affected examples before calling the skill reusable.
- If the voice gender, age, delivery style, or emotion clashes with the topic, replace the voice or label the render draft.
- If the ending has 3-5 seconds of silent/empty tail, idle picture, or subtitle/audio mismatch, shorten the composition or add an intentional closing beat before delivery.
- If the final MP4 is missing or ffprobe cannot see video and audio streams, delivery failed.
- If a reported defect was fixed only in source assets but the final MP4 was not re-rendered and checked, delivery is incomplete.
- If the V4.5 scorecard has a blocking item below 3/5, delivery is incomplete.
- If template assets only cover one narrow topic and the user asked for a reusable/shareable skill, update the template family matrix before calling the skill complete.

## Resources

- `scripts/install_env.sh`: first-time local dependency installer/checker.
- `scripts/create_project.py`: creates a Remotion project with draft placeholders and validation scripts.
- `scripts/prefetch_f5tts.py`: predownloads default F5-TTS/Vocos model files.
- `references/production-checklist.md`: detailed release checklist.
