# 纸片分层动画生成Skill

![纸片分层动画Skill 封面](assets/cover.png)

一个通用的纸片分层动画视频生成 Skill，用于把任意主题转成具有纸片质感、分层素材、动态入场、旁白配音、中文字幕和 MP4 交付的短视频工作流。

这个 Skill 重点解决以下问题：

- 纸片视频不能只是静态图片加淡入淡出；
- 人物、背景、道具、烟雾、前景纸片等必须分层；
- 透明 PNG 不能有脏边、残留、矩形透明块；
- 字幕必须和最终旁白对齐；
- 旁白不能只有一种默认音色；
- 成片必须经过 ffprobe、运动密度、音频、字幕、抠图等质量检查。

## 适用场景

- 历史人物 / 传记
- 战争 / 策略 / 军事
- 商业案例 / 产品广告
- 教育 / 科普 / 知识讲解
- 民间故事 / 神话 / 叙事短片
- 美食 / 生活 / 旅行
- 娱乐 / 社媒 / 热点内容
- 新闻 / 时事 / 观点解释

## 当前能力等级

V4.8 voice-palette quality gate

核心质量门禁包括：

- V4.4：抠图残留、字幕错字、机器人配音、静态画面等缺陷处理；
- V4.5：风格手册、主角包、场景分层清单、参考视频对齐；
- V4.6：自动化 QA 工具和多题材模板资产系统；
- V4.7：纸张纹理、毛边、阴影、道具词汇、资产美术层升级；
- V4.8：多性别、多年龄段、多题材适配的旁白音色库。

## 目录结构

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── CONTRIBUTORS.md
├── references/
│   └── production-checklist.md
├── scripts/
│   ├── install_env.sh
│   ├── create_project.py
│   └── prefetch_f5tts.py
└── templates/
    ├── config/
    │   └── voice_profiles.json
    └── scripts/
        ├── audit_cutout_alpha.py
        ├── make_cutout_checker_sheet.py
        ├── motion_density_check.py
        ├── subtitle_sync_audit.py
        ├── audio_loudness_check.sh
        └── voice_palette_audit.py
```

## 快速开始

### 1. 安装环境

```bash
bash scripts/install_env.sh
```

这个脚本会检查或安装常用依赖，包括 Node.js、FFmpeg、Python 环境、Remotion 相关依赖，以及可选的 F5-TTS 环境。

### 2. 创建一个纸片动画项目

```bash
python3 scripts/create_project.py ./demo-paper-video \
  --title "西施的故事" \
  --theme "春秋末年的历史人物纸片动画" \
  --width 1080 \
  --height 1440 \
  --duration 1800
```

### 3. 进入项目并安装依赖

```bash
cd demo-paper-video
npm install
```

### 4. 根据主题补全资产与分层

生成最终视频前，必须完成：

- 风格手册；
- 主角角色包；
- 每个场景的 Layer Manifest；
- 透明 PNG / WebP 分层素材；
- 旁白脚本和字幕文本；
- 音色选择；
- QA 脚本配置。

### 5. 渲染与检查

```bash
npm run render
npm run check
```

如果项目中使用了本仓库提供的 QA 工具，建议额外运行：

```bash
python3 scripts/make_cutout_checker_sheet.py public/assets out/cutouts-checker.jpg
python3 scripts/audit_cutout_alpha.py public/assets --out out/alpha-audit.json
python3 scripts/motion_density_check.py out/final.mp4 --out out/motion-density.csv
python3 scripts/subtitle_sync_audit.py src/captions.ts public/audio/narration.wav
python3 scripts/voice_palette_audit.py --config voice_profiles.json
bash scripts/audio_loudness_check.sh out/final.mp4
```

## 音色库

`templates/config/voice_profiles.json` 提供了 16 个中文/华语旁白音色配置，覆盖：

- 男声 / 女声；
- 儿童、年轻成人、成熟成人；
- 大陆普通话、东北普通话、陕西/中原普通话、台湾普通话、香港/粤语方向；
- 历史纪录片、商业讲解、温暖生活、科普教育、新闻纪录片、戏剧故事、地方文化、娱乐社媒等风格。

实际项目中不要把所有视频都固定成一个音色。应根据题材、受众和情绪选择 voice profile。

## 质量底线

以下情况不能作为最终成片交付：

- 主角缺失、丑、前后不一致；
- 抠图边缘有残留物、脏块、矩形透明块；
- 人物、背景、道具没有分层动画；
- 只有淡入淡出，没有纸片物理感；
- 字幕错字、缺失、和旁白不同步；
- 旁白机器人味重、音色和题材不匹配；
- 最后 3-5 秒空停、无声、无字幕、无视觉收束；
- 没有经过 ffprobe、音频、字幕、运动密度、alpha 审计等检查。

## 贡献者

majiabin2020

## License

MIT License
