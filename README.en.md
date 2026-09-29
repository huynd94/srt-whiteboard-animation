# SRT Whiteboard Animation Skill

[Tiếng Việt (default)](README.md) | **English**

Turn SRT subtitles into hand-drawn whiteboard videos drawn in narrative order. The skill combines **region-mask orchestration** with **continuous stream strokes**: each element appears in subtitle order, the pen lays down ink continuously within its region, then adds color, before exporting MP4.

Suitable for turning knowledge explainers, spoken stories, course subtitles, or short-video scripts into hand-drawn animation on warm beige paper.

## Example output

**Scene: a banana snatch on Monkey Mountain** — following the subtitle narrative, draw the rockery and small monkey, the large monkey stealing the banana, then the children watching. Original example names and data are preserved.

![Banana snatch on Monkey Mountain: SRT whiteboard animation demo](examples/scene-01-monkey-mountain-stream.gif)

Original line art: [view PNG](examples/scene-01-monkey-mountain.png).

## Core capabilities

- Parse SRT and suggest scenes lasting 25–35 seconds.
- Present a storyboard and illustration strategy first, with one core idea per scene.
- Order drawing by subtitle events rather than image coordinates.
- Manage regions, timing, subtitle links, and overlap protection with `annotation.json`.
- Draw continuous strokes in each region: `ink` for line art, then `color` for coloring.
- Adjust regions, order, timing, and subtitle links in a browser preview editor.
- Render individual scenes and merge multiple scenes into a complete MP4.

## Vietnamese/English localization

Vietnamese with diacritics is the default (`vi`); English (`en`) is used only when explicitly requested. Guidance, storyboards, and newly generated descriptions (`storyBasis`, `label`, `narrativeRole`) follow the selected language. **Source subtitles and the `subtitle` field remain unchanged**; switching language does not translate them. JSON keys, technical identifiers, and original examples are preserved.

All six Python scripts accept `--lang vi` or `--lang en` (default: `vi`):

| Script | Purpose |
|---|---|
| `scripts/prepare_env.py` | Check/prepare the Python environment |
| `scripts/parse_srt.py` | Parse subtitles and suggest scenes |
| `scripts/render_annotation_preview.py` | Generate annotation inspection images |
| `scripts/render_stream_whiteboard.py` | Render MP4 from annotated regions |
| `scripts/stream_render.py` | Low-level whole-image stream renderer |
| `scripts/merge_scenes.py` | Merge MP4 files in order |

`--lang` selects CLI messages/help and generated descriptions; it does not translate source data or existing annotations. Machine-readable output markers such as `ENV_PY=` and `OUTPUT=` remain unchanged.

In `assets/preview.html`, use the Vietnamese/English language selector. The choice is saved in `localStorage` for subsequent visits; the first visit defaults to Vietnamese. The UI selection is independent of the CLI's `--lang` option.

SRT and annotation JSON inputs use **UTF-8**, including **UTF-8 with BOM** (common when saving files from Windows PowerShell 5.1). The bundled `assets/fonts/NotoSans-Regular.ttf` is used by the browser and Pillow to display Vietnamese diacritics. Preserve the font's accompanying license; VI/EN support does not imply coverage of every script found in source subtitles.

Default prompt:

```text
Dùng $srt-whiteboard-animation tạo hoạt ảnh vẽ tay trên bảng trắng từ phụ đề SRT này. Dùng tiếng Việt cho phần hướng dẫn và mô tả, giữ nguyên phụ đề nguồn và chờ xác nhận sau mỗi bước.
```

To explicitly request English:

```text
Use $srt-whiteboard-animation to create a hand-drawn whiteboard animation from this SRT. Use English for guidance and generated descriptions, keep the source subtitles unchanged, and wait for confirmation after each step.
```

## How it works

The key principle is **subtitle-driven production with confirmation at each step**. Stop after each step and wait for explicit user confirmation to avoid rendering before the storyboard, line art, or annotations are final. [SKILL.md](SKILL.md) is the authoritative workflow and full set of constraints.

1. Parse SRT and present the storyboard and illustration strategy; wait for confirmation.
2. After confirmation, generate consistently styled line art; wait for approval of the line art.
3. After line-art approval, read the subtitles, inspect the original image, and create annotations; immediately open the preview editor and load the annotation directory. Wait for confirmation of the annotations and preview content.
4. After confirmation, generate region/direction inspection images; wait for approval of those images.
5. After approval, adjust regions, narrative order, timing, and subtitle links in the preview editor, then save; wait for confirmation of the final annotations and timing.
6. After final confirmation, render each scene to MP4; wait for approval of the rendered scenes.
7. For multi-scene projects, merge only after every rendered scene has been approved; wait for approval of the final combined video.

Silence, earlier blanket permission, and lack of objection do not count as confirmation. When a previous step needs revision, redo only that step and await fresh confirmation. Opening and loading the preview editor immediately after JSON creation is part of step 3, not a separate approval gate.

## Visual guidelines

- Warm beige paper background, preferably `#F5EBD7`.
- Dark gray sketch lines; red, orange, and blue only as small conceptual accents.
- Minimal hand-drawn art, a clean background, and ample whitespace.
- No text/labels in scene source images, photographic appearance, 3D effects, or complex textures.

## Installation and environment

The skill includes a dedicated Python virtual-environment setup script. Run these commands from the repository root in **Windows PowerShell**:

```powershell
python scripts/prepare_env.py --check --lang en
# If the check reports a missing environment/dependency, run:
python scripts/prepare_env.py --lang en
```

On success, the final line prints `ENV_PY=<python-path>`. Use that interpreter for subsequent commands to keep dependencies isolated. The setup script installs the required dependencies, including OpenCV, NumPy, PyAV, and Pillow.

**About `ENV_PY`:** this is text output, not an automatic PowerShell or environment-variable assignment. Assign the reported path to `$ENV_PY`; adjust the example below if the skill is installed elsewhere. The `&` call operator also handles paths containing spaces:

```powershell
$ENV_PY = 'D:\Project\srt-whiteboard-animation\.venv\Scripts\python.exe'
& $ENV_PY scripts/parse_srt.py --help --lang en
```

## Project asset structure

```text
assets/whiteboard/<project-name>/
├── scene-01-<name>.png
├── scene-01-<name>.annotation.json
├── scene-01-<name>-whiteboard.mp4
└── scene-01-<name>-preview.mp4
```

Images and annotations must share a base name; for example, `scene-01-demo.png` pairs with `scene-01-demo.annotation.json`.

## Annotation format

Each element uses integer pixel coordinates from the original image and links to subtitle events through `sequence`, `subtitle`, and `narrativeRole`. Order regions as “scene setup → key character/object → action or change → reaction/result”.

The original example below is preserved, including its Chinese content. Newly generated descriptions follow the selected language; subtitles always follow the source.

```json
{
  "sceneId": "scene-01",
  "canvas": { "width": 1672, "height": 941 },
  "storyBasis": "小猴在猴子山上拿着香蕉，大猴抢走香蕉，孩子们在旁观看。",
  "sceneDurationMs": 9000,
  "elements": [
    {
      "id": "rockery",
      "label": "猴子山场景",
      "sequence": 1,
      "narrativeRole": "故事的场景铺垫",
      "subtitle": "小猴子坐在猴子山顶，手里拿着香蕉。",
      "type": "structure",
      "region": { "x": 20, "y": 120, "width": 540, "height": 780 },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 300,
        "durationMs": 2600,
        "maskPaddingPx": 22,
        "protectedRegions": []
      },
      "handPath": { "start": [290, 130], "end": [290, 890], "easing": "easeInOut" }
    }
  ]
}
```

`direction` and `handPath` are used by the preview editor's rectangular proxy; the stream renderer automatically generates the final video's real strokes. For mutually occluding objects, mark areas that must appear later in the earlier element's `protectedRegions` to prevent subsequent content from appearing early.

## Common commands

Replace example filenames with actual paths. These single-line commands work in PowerShell and explicitly select English with `--lang en`; use `--lang vi` for Vietnamese.

Parse subtitles and suggest scenes:

```powershell
& $ENV_PY scripts/parse_srt.py 'input.srt' --target-sec 30 --min-sec 25 --max-sec 35 --lang en
```

Generate a region inspection image:

```powershell
& $ENV_PY scripts/render_annotation_preview.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-regions.png' --lang en
```

Open `assets/preview.html` in Chrome/Edge and use the open-folder action to load a scene directory, then edit regions, order, timing, and subtitle links. No server is required. Writing directly to files requires the File System Access API; in other browsers, download the files and replace the originals manually.

Render one scene:

```powershell
& $ENV_PY scripts/render_stream_whiteboard.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-whiteboard.mp4' 'assets/drawing-hand.png' --ink-path grid --color-fill contour-wipe --lang en
```

Without `--total-ms`, the renderer uses the annotation's `sceneDurationMs`; the final line prints `OUTPUT=<path>`.

Low-level whole-image stream renderer (standalone use, not a replacement for the region-annotation workflow):

```powershell
& $ENV_PY scripts/stream_render.py 'scene-01.png' --out-dir 'out' --total-ms 9000 --lang en
```

Merge multiple scenes:

```powershell
& $ENV_PY scripts/merge_scenes.py --inputs 'scene-01-whiteboard.mp4' 'scene-02-whiteboard.mp4' 'scene-03-whiteboard.mp4' --output 'final.mp4' --lang en
```

## Quality checks

- The first frame is clean warm beige paper, with no prematurely visible lines.
- `canvas` matches the original image size; all regions use integer pixel coordinates within the canvas.
- `sequence` and `startMs` follow the subtitle narrative.
- In intermediate frames, unstarted regions and protected areas do not appear early.
- The pen tip stays close to the current stream stroke; use `--ink-path skeleton` for clear line art if appropriate.
- Each scene holds the complete image for at least 0.5 seconds at the end; merged scenes follow the subtitle storyboard order.

## Repository contents

```text
srt-whiteboard-animation/
├── README.md                         # Vietnamese documentation (default)
├── README.en.md                      # Equivalent English documentation
├── SKILL.md                          # Authoritative workflow and constraints
├── assets/
│   ├── drawing-hand.png              # Drawing-hand asset
│   ├── fonts/NotoSans-Regular.ttf    # Browser and Pillow font
│   └── preview.html                  # Local preview/editor
├── examples/                         # Original README example assets
├── scripts/
│   ├── parse_srt.py                  # Subtitle parsing and scene suggestions
│   ├── render_annotation_preview.py  # Annotation inspection images
│   ├── render_stream_whiteboard.py   # Region-based MP4 renderer
│   ├── stream_render.py              # Low-level whole-image stream renderer
│   ├── merge_scenes.py               # Multi-scene merging
│   └── prepare_env.py                # Dependency environment setup
└── agents/openai.yaml                # Codex metadata, Vietnamese by default
```

## Contributing

Issues and pull requests are welcome. Any drawing-logic change should be checked with real subtitles, annotations, and rendered videos to verify mask protection, timing, and the final image.

## License

This project is open source under the MIT License; see [LICENSE](LICENSE). The bundled font has its own license in `assets/fonts/`.

## About the author

The original introduction and account name are preserved for accurate attribution:

一个爱养鱼的老登 / AI Builder / 用 AI 团队打造一人公司。

抖音、B站、公众号：江哥是老登啊

Approximate translation: a fishkeeping enthusiast / AI Builder / building a one-person company with an AI team. The author uses **江哥是老登啊** on Douyin, Bilibili, and their WeChat public account.
