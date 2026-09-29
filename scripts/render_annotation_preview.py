import json
import sys
from pathlib import Path

from i18n import ArgumentParser, run_cli, t

DEFAULT_FONT = Path(__file__).resolve().parents[1] / 'assets' / 'fonts' / 'NotoSans-Regular.ttf'


def draw_label(overlay, text, box, font, color):
    """Wrap using glyph bounds and clip to a bounded layer, including tiny regions."""
    from PIL import Image, ImageDraw
    left, top, right, bottom = map(int, box)
    left, top = max(0, left), max(0, top)
    right, bottom = min(overlay.width, right), min(overlay.height, bottom)
    width, height = right - left, bottom - top
    if width <= 8 or height <= 8:
        return
    layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    available = width - 8
    lines, line = [], ''
    # Character wrapping also handles unspaced labels and CJK with a supplied font.
    for char in text:
        bounds = draw.textbbox((0, 0), line + char, font=font)
        if char == '\n' or (line and bounds[2] - bounds[0] > available):
            lines.append(line)
            line = '' if char == '\n' else char
        else:
            line += char
    if line:
        lines.append(line)
    bounds = draw.textbbox((0, 0), 'Áỵ', font=font)
    line_height = bounds[3] - bounds[1] + 4
    count = max(0, (height - 8) // line_height)
    if not count:
        return
    visible = lines[:count]
    if len(lines) > count:
        last = visible[-1]
        while last and draw.textbbox((0, 0), last + '…', font=font)[2] > available:
            last = last[:-1]
        visible[-1] = last + '…'
    draw.rounded_rectangle((0, 0, width - 1, min(height - 1, len(visible) * line_height + 7)),
                           radius=6, fill=(255, 255, 255, 225))
    for index, line in enumerate(visible):
        bbox = draw.textbbox((0, 0), line, font=font)
        draw.text((4 - bbox[0], 4 + index * line_height - bbox[1]), line, font=font, fill=color)
    overlay.alpha_composite(layer, (left, top))


def main(image_path: str, annotation_path: str, output_path: str, font_path=None) -> None:
    from PIL import Image, ImageDraw, ImageFont
    with Image.open(image_path) as source:
        image = source.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_file = str(font_path or DEFAULT_FONT)
    try:
        small_font = ImageFont.truetype(font_file, 18)
    except OSError as error:
        raise OSError(t('font_error', path=font_file)) from error
    colors = [(38, 103, 255, 225), (255, 105, 92, 225), (41, 167, 102, 225), (181, 100, 255, 225)]

    data = json.loads(Path(annotation_path).read_text(encoding="utf-8-sig"))
    for index, element in enumerate(data["elements"], start=1):
        region = element["region"]
        x, y = region["x"], region["y"]
        right, bottom = x + region["width"], y + region["height"]
        color = colors[(index - 1) % len(colors)]
        fill = (*color[:3], 24)
        draw.rounded_rectangle((x, y, right, bottom), radius=12, outline=color, width=4, fill=fill)
        draw.ellipse((x + 8, y + 8, x + 44, y + 44), fill=color)
        draw.text((x + 19, y + 8), str(index), anchor="ma", font=small_font, fill="white")
        label = f"{index}. {element['label']}  {t(element['reveal']['direction'])}"
        draw_label(overlay, label, (x + 52, y + 8, right - 8, bottom - 8), small_font, color)
        start = tuple(element["handPath"]["start"])
        end = tuple(element["handPath"]["end"])
        draw.line((start, end), fill=color, width=4)
        draw.polygon((end, (end[0] - 13, end[1] - 7), (end[0] - 13, end[1] + 7)), fill=color)

    result = Image.alpha_composite(image, overlay).convert("RGB")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path, quality=95)


def cli(argv=None):
    parser = ArgumentParser(argv=argv, description='preview')
    parser.add_argument('image', help='线稿图路径')
    parser.add_argument('annotation', help='同名 annotation.json 路径')
    parser.add_argument('output', help='preview_output')
    parser.add_argument('--font', default=str(DEFAULT_FONT), help='font')
    args = parser.parse_args(argv)
    main(args.image, args.annotation, args.output, args.font)
    return 0


if __name__ == "__main__":
    sys.exit(run_cli(cli))
