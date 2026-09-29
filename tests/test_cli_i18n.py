"""CLI contracts exercised in fresh processes, including ASCII-configured pipes."""
import importlib.util
import json
import os
from pathlib import Path
import string
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import i18n

NAMES = ('parse_srt', 'prepare_env', 'render_annotation_preview',
         'render_stream_whiteboard', 'stream_render', 'merge_scenes')


def cli(name, *args, no_site=False):
    env = dict(os.environ, PYTHONIOENCODING='ascii', PYTHONUTF8='0')
    return subprocess.run([sys.executable, *(['-S'] if no_site else []),
                           str(SCRIPTS / (name + '.py')), *map(str, args)],
                          capture_output=True, env=env, timeout=60)


class CLIIntegrationTests(unittest.TestCase):
    def test_help_all_scripts_without_third_party_dependencies(self):
        for name in NAMES:
            for language in ('vi', 'en'):
                for args in (('--lang', language, '--help'), ('--help', '--lang=' + language)):
                    with self.subTest(script=name, args=args):
                        result = cli(name, *args, no_site=True)
                        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
                        text = result.stdout.decode('utf-8')
                        self.assertIn('cách dùng:' if language == 'vi' else 'usage:', text)
                        self.assertIn('--lang', text)
                        self.assertNotRegex(text, '[\u4e00-\u9fff]')
                        self.assertEqual(result.stderr, b'')
            default = cli(name, '--help', no_site=True)
            self.assertIn('cách dùng:', default.stdout.decode('utf-8'))

    def test_invalid_language_and_missing_values_are_usage_errors(self):
        for name in NAMES:
            for args, marker in ((('--lang', 'xx'), 'lỗi:'),
                                 (('--lang',), 'lỗi:'),
                                 (('--lang', 'en', '--unknown-option'), 'error:')):
                with self.subTest(script=name, args=args):
                    result = cli(name, *args, no_site=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn(marker, result.stderr.decode('utf-8'))
                    self.assertNotIn(b'Traceback', result.stderr)

    def test_bom_unicode_paths_json_stdout_and_language_invariant_data(self):
        with tempfile.TemporaryDirectory(prefix='phụ đề 中文 ') as tmp:
            source = Path(tmp) / 'bài học 中文.srt'
            source.write_bytes(('1\r\n00:00:01,000 --> 00:00:03,500\r\n'
                                'Tiếng Việt: Nguyễn, đường phố 中文 🌱\r\n').encode('utf-8-sig'))
            outputs = []
            for language in ('vi', 'en'):
                result = cli('parse_srt', source, '--lang', language)
                self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
                self.assertIn('Nguyễn'.encode('utf-8'), result.stdout)
                self.assertFalse(result.stdout.startswith(b'\xef\xbb\xbf'))
                outputs.append(json.loads(result.stdout.decode('utf-8')))
                self.assertIn('Phụ đề:' if language == 'vi' else 'Cues:', result.stderr.decode('utf-8'))
            self.assertEqual(outputs[0], outputs[1])
            self.assertEqual(outputs[0]['cues'][0], {
                'index': 1, 'startMs': 1000, 'endMs': 3500, 'durMs': 2500,
                'text': 'Tiếng Việt: Nguyễn, đường phố 中文 🌱'})
            self.assertEqual(outputs[0]['scenes'][0]['sceneDurationMs'], 2500)

    def test_invalid_utf8_is_clear_and_keeps_stdout_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'invalid.srt'
            source.write_bytes(b'\xff\xfe\x80')
            for language in ('vi', 'en'):
                result = cli('parse_srt', source, '--lang', language)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, b'')
                self.assertIn('UTF-8', result.stderr.decode('utf-8'))
                self.assertNotIn(b'Traceback', result.stderr)

    def test_catalog_parity_and_format_placeholders(self):
        self.assertEqual(i18n.CATALOGS['vi'].keys(), i18n.CATALOGS['en'].keys())
        formatter = string.Formatter()
        for key, vi in i18n.CATALOGS['vi'].items():
            en = i18n.CATALOGS['en'][key]
            fields = lambda text: {(field, spec, conversion) for _, field, spec, conversion
                                   in formatter.parse(text) if field is not None}
            with self.subTest(key=key):
                self.assertTrue(vi)
                self.assertTrue(en)
                self.assertEqual(fields(vi), fields(en))
                self.assertNotRegex(vi + en, '[\u4e00-\u9fff]')

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'Pillow is unavailable')
    def test_annotation_bom_vietnamese_png_and_narrow_labels(self):
        from PIL import Image, ImageChops
        font = ROOT / 'assets' / 'fonts' / 'NotoSans-Regular.ttf'
        if not font.exists():
            self.skipTest('Parent-supplied NotoSans-Regular.ttf is unavailable')
        with tempfile.TemporaryDirectory(prefix='chú thích ') as tmp:
            image, annotation, output = [Path(tmp) / name for name in ('ảnh.png', 'vùng.json', 'kết quả.png')]
            Image.new('RGB', (400, 180), 'white').save(image)
            # Short label so translated direction text is visible and vi/en images differ.
            elements = []
            for x, width in ((0, 320), (330, 15)):
                elements.append({'label': 'Nguyễn',
                                 'region': {'x': x, 'y': 5, 'width': width, 'height': 150},
                                 'reveal': {'direction': 'left-to-right'},
                                 'handPath': {'start': [x + 2, 100], 'end': [x + width - 2, 130]}})
            annotation.write_text(json.dumps({'elements': elements}, ensure_ascii=False), encoding='utf-8-sig')
            result = cli('render_annotation_preview', image, annotation, output)
            self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
            with Image.open(output) as rendered:
                self.assertEqual(rendered.format, 'PNG')
                self.assertEqual(rendered.size, (400, 180))
                self.assertIsNotNone(ImageChops.difference(rendered.convert('RGB'), Image.new('RGB', rendered.size, 'white')).getbbox())
            english = Path(tmp) / 'english.png'
            result = cli('render_annotation_preview', image, annotation, english, '--lang', 'en', '--font', font)
            self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
            self.assertNotEqual(output.read_bytes(), english.read_bytes())


if __name__ == '__main__':
    unittest.main()
