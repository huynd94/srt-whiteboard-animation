"""Shared, dependency-free CLI language and UTF-8 boundary handling."""
from __future__ import annotations

import argparse
import sys

# Source messages are stable catalog keys; data and CLI option values are never translated.
MESSAGES = {
    'lang': ('Ngôn ngữ giao diện (mặc định: vi)', 'Interface language (default: vi)'),
    'failure': ('[err] Không thể hoàn tất: {error}', '[err] Unable to complete: {error}'),
    'unicode': ('[err] Lỗi Unicode: hãy dùng dữ liệu UTF-8 (có thể có BOM). {error}', '[err] Unicode error: use UTF-8 data (BOM is accepted). {error}'),
    'dependency': ('[err] Thiếu thư viện: {error}', '[err] Missing dependency: {error}'),
    'prepare': ('Chuẩn bị môi trường Python và các thư viện', 'Prepare the Python environment and dependencies'),
    'check': ('Chỉ kiểm tra; không tạo môi trường hoặc cài thư viện', 'Check only; do not create an environment or install dependencies'),
    'preview': ('Tạo ảnh xem trước các vùng chú thích', 'Render an annotation region preview'),
    'font': ('Phông TTF/OTF thay thế (ví dụ phông hỗ trợ CJK)', 'Alternative TTF/OTF font (for example, a CJK-capable font)'),
    'font_error': ('Không tải được phông {path}; dùng --font để chọn phông TTF/OTF khác', 'Cannot load font {path}; use --font to select another TTF/OTF font'),
    'preview_output': ('Đường dẫn ảnh đầu ra', 'Output image path'),
    'SRT 解析 + 分镜建议': ('Phân tích SRT và gợi ý phân cảnh', 'Parse SRT and suggest scenes'),
    '字幕文件路径 (.srt)': ('Đường dẫn phụ đề (.srt)', 'Subtitle file path (.srt)'),
    '每幕目标口播秒数（默认 30）': ('Thời lượng mục tiêu mỗi cảnh, giây (mặc định 30)', 'Target seconds per scene (default 30)'),
    '每幕最短秒数（默认 25）': ('Thời lượng tối thiểu mỗi cảnh, giây (mặc định 25)', 'Minimum seconds per scene (default 25)'),
    '每幕最长秒数（默认 35）': ('Thời lượng tối đa mỗi cảnh, giây (mặc định 35)', 'Maximum seconds per scene (default 35)'),
    '按顺序合并多幕白板动画 MP4': ('Ghép các cảnh hoạt hình bảng trắng MP4 theo thứ tự', 'Merge whiteboard MP4 scenes in order'),
    '按播放顺序的 MP4 列表': ('Danh sách MP4 theo thứ tự phát', 'MP4 files in playback order'),
    '合并输出路径': ('Đường dẫn video đã ghép', 'Merged output path'),
    'SRT 白板动画整合渲染器（mask 编排 + stream 画法）': ('Kết xuất hoạt hình bảng trắng SRT (vùng mặt nạ và nét vẽ liên tục)', 'SRT whiteboard renderer (mask sequencing and continuous strokes)'),
    '线稿图路径': ('Đường dẫn ảnh nét vẽ', 'Line-art image path'),
    '同名 annotation.json 路径': ('Đường dẫn annotation.json tương ứng', 'Matching annotation.json path'),
    '输出 MP4 路径': ('Đường dẫn MP4 đầu ra', 'Output MP4 path'),
    '手部素材 PNG（默认内置）': ('Ảnh bàn tay PNG (mặc định dùng ảnh đi kèm)', 'Hand PNG (bundled image by default)'),
    '总时长；缺省用标注 sceneDurationMs': ('Tổng thời lượng ms; mặc định lấy sceneDurationMs', 'Total milliseconds; defaults to annotation sceneDurationMs'),
    '不叠加笔尖/手部': ('Không hiển thị đầu bút/bàn tay', 'Do not overlay the pen/hand'),
    '笔迹路径: grid 网格(默认); skeleton 骨架追踪': ('Đường nét: grid lưới (mặc định); skeleton bám khung nét', 'Stroke path: grid (default); skeleton tracing'),
    '上色: contour-wipe 轮廓扫描(默认); brush 沿轨迹刷': ('Tô màu: contour-wipe quét theo viền (mặc định); brush theo nét', 'Color: contour-wipe scan (default); brush along strokes'),
    '起笔段停顿节奏（预留，逐区域画法下影响较弱）': ('Nhịp dừng khi vẽ (ít ảnh hưởng trong chế độ theo vùng)', 'Ink pause rhythm (limited effect in per-region rendering)'),
    '输出长边像素上限（预览可调小加速，默认 1080）': ('Giới hạn cạnh dài đầu ra, pixel (mặc định 1080; giảm để xem trước nhanh)', 'Maximum output long edge in pixels (default 1080; lower for faster previews)'),
    '把一张图片渲染成流式笔迹白板动画视频': ('Kết xuất ảnh thành video bảng trắng với nét vẽ liên tục', 'Render an image as a continuous-stroke whiteboard video'),
    '输入图片路径 (PNG/JPG/JPEG/BMP/TIFF)': ('Đường dẫn ảnh đầu vào (PNG/JPG/JPEG/BMP/TIFF)', 'Input image path (PNG/JPG/JPEG/BMP/TIFF)'),
    '输出目录 (默认: ./out)': ('Thư mục đầu ra (mặc định: ./out)', 'Output directory (default: ./out)'),
    '视频总时长，单位毫秒 (默认: 10000)': ('Tổng thời lượng video, mili giây (mặc định: 10000)', 'Total video duration in milliseconds (default: 10000)'),
    '不叠加笔尖/手部覆盖': ('Không hiển thị đầu bút/bàn tay', 'Do not overlay the pen/hand'),
    '自定义笔尖/手部素材路径 (默认: skill 内置 drawing-hand.png)': ('Ảnh đầu bút/bàn tay tùy chọn (mặc định: drawing-hand.png đi kèm)', 'Custom pen/hand image (default: bundled drawing-hand.png)'),
    '覆盖默认帧率': ('Thay tốc độ khung hình mặc định', 'Override the default frame rate'),
    '覆盖默认网格边长': ('Thay kích thước ô lưới mặc định', 'Override the default grid edge'),
    '覆盖默认墨刷半径': ('Thay bán kính bút mặc định', 'Override the default brush radius'),
    '添彩阶段上色风格: contour-wipe 轮廓感知自上而下扫描 (默认); brush 沿笔画轨迹刷': ('Tô màu: contour-wipe quét từ trên xuống theo viền (mặc định); brush theo nét', 'Color style: contour-wipe top-down contour scan (default); brush along strokes'),
    'contour-wipe: 阻力场逐行向下衰减系数 (默认 0.86，越小越快越过轮廓)': ('contour-wipe: hệ số giảm lực cản từng hàng (mặc định 0.86; nhỏ hơn vượt viền nhanh hơn)', 'contour-wipe: per-row resistance decay (default 0.86; smaller crosses contours faster)'),
    'contour-wipe: 轮廓处前沿扣减比例×h (默认 0.04，越大轮廓处停留越久)': ('contour-wipe: tỷ lệ trễ tại viền × chiều cao (mặc định 0.04; lớn hơn dừng lâu hơn)', 'contour-wipe: contour delay ratio × height (default 0.04; larger pauses longer)'),
    'contour-wipe: 笔尖横向来回扫动趟数 (默认 18)': ('contour-wipe: số lượt quét ngang (mặc định 18)', 'contour-wipe: horizontal sweep count (default 18)'),
    '起笔段停顿节奏: heavy 明显(默认); auto 按密度自动分档; off 关闭; light 少量': ('Nhịp dừng: heavy rõ (mặc định); auto theo mật độ; off tắt; light nhẹ', 'Ink pauses: heavy (default); auto by density; off disabled; light sparse'),
    '起笔段笔迹路径: grid 网格格中心插值(默认); skeleton 骨架级像素追踪(更精准贴合线条)': ('Đường nét: grid nội suy tâm ô (mặc định); skeleton bám khung pixel chính xác hơn', 'Ink path: grid cell-center interpolation (default); skeleton pixel tracing (closer to lines)'),
    'read_srt': ('[err] Không đọc được phụ đề: {error}', '[err] Cannot read subtitles: {error}'),
    'no_cues': ('[err] Không có mục phụ đề; hãy kiểm tra định dạng SRT', '[err] No subtitle cues found; check the SRT format'),
    'summary': ('Phụ đề: {count}  Tổng thời lượng: {seconds:.1f}s  Cảnh gợi ý: {scenes}', 'Cues: {count}  Total duration: {seconds:.1f}s  Suggested scenes: {scenes}'),
    'scene': ('  Cảnh {index:>2}  {start:6.1f}-{end:6.1f}s ({duration:4.1f}s, phụ đề {first}-{last}): {text}', '  Scene {index:>2}  {start:6.1f}-{end:6.1f}s ({duration:4.1f}s, cues {first}-{last}): {text}'),
    'reuse_env': ('[ok] Dùng lại môi trường: {path}', '[ok] Reusing environment: {path}'),
    'no_env': ('[err] Chưa tạo môi trường: {path}', '[err] Environment not created: {path}'),
    'create_env': ('[..] Đang tạo môi trường: {path}', '[..] Creating environment: {path}'),
    'env_ready': ('[ok] Môi trường đã sẵn sàng', '[ok] Environment ready'),
    'install': ('[..] Cài thư viện: {packages}', '[..] Installing dependencies: {packages}'),
    'install_failed': ('[err] Cài đặt thất bại:\n{error}', '[err] Installation failed:\n{error}'),
    'installed': ('[ok] Đã cài thư viện', '[ok] Dependencies installed'),
    'missing_deps': ('\nThiếu {count} thư viện: {packages}', '\nMissing {count} dependencies: {packages}'),
    'merge_copy': ('  ffmpeg đã ghép không mất dữ liệu: {path}', '  ffmpeg lossless merge complete: {path}'),
    'merge_retry': ('  [warn] ffmpeg -c copy thất bại, thử mã hóa lại: {error}', '  [warn] ffmpeg -c copy failed, trying re-encoding: {error}'),
    'merge_encoded': ('  ffmpeg đã ghép và mã hóa lại: {path}', '  ffmpeg re-encoded merge complete: {path}'),
    'merge_failed': ('  [warn] ffmpeg mã hóa lại thất bại: {error}', '  [warn] ffmpeg re-encoding failed: {error}'),
    'merge_av': ('  PyAV đã ghép xong: {path}', '  PyAV merge complete: {path}'),
    'missing_inputs': ('[err] Thiếu tệp đầu vào: {paths}', '[err] Missing input files: {paths}'),
    'no_merger': ('[err] Ghép thất bại: không có ffmpeg và PyAV không khả dụng', '[err] Merge failed: ffmpeg is absent and PyAV is unavailable'),
    'bad_color': ('Màu không hợp lệ: {color}', 'Invalid color: {color}'),
    'grid_size': ('Kích thước ảnh {w}x{h} phải là bội số của {edge}', 'Image size {w}x{h} must be a multiple of {edge}'),
    'no_skeleton': ('  [warn] Không có nét khung; chuyển sang đường tâm ô', '  [warn] No skeleton strokes; falling back to cell-center paths'),
    'skeleton': ('  Bám khung: {count} nét, {points} điểm mẫu', '  Skeleton tracing: {count} strokes, {points} sample points'),
    'no_ink': ('  Không có nét mực; bỏ qua bước vẽ', '  No ink; skipping the ink phase'),
    'no_skeleton_phase': ('  Không có nét khung; bỏ qua bước vẽ', '  No skeleton strokes; skipping the ink phase'),
    'pauses': ('  Dừng thích ứng: {count} khung hình (chế độ={mode})', '  Adaptive pauses: {count} frozen frames (mode={mode})'),
    'ink_progress': ('  Tiến độ vẽ: {percent}%', '  Ink progress: {percent}%'),
    'ink_done': ('  Đã vẽ: {count} ô, {frames} khung hình', '  Ink complete: {count} cells, {frames} frames'),
    'skeleton_done': ('  Đã vẽ khung: {count} điểm mẫu, {frames} khung hình', '  Skeleton ink complete: {count} sample points, {frames} frames'),
    'no_color': ('  Không có nét mực; bỏ qua bước tô màu', '  No ink; skipping the color phase'),
    'color_progress': ('  Tiến độ tô màu: {percent}%', '  Color progress: {percent}%'),
    'color_done': ('  Đã tô màu: {count} ô, {frames} khung hình', '  Color complete: {count} cells, {frames} frames'),
    'no_wipe': ('  Không có khung tô màu; bỏ qua contour-wipe', '  No color frames; skipping contour-wipe'),
    'wipe': ('  contour-wipe: {w}x{h}, delay_px={delay}, lượt quét={blocks}', '  contour-wipe: {w}x{h}, delay_px={delay}, sweeps={blocks}'),
    'wipe_progress': ('  Tiến độ tô màu (contour-wipe): {percent}%', '  Color progress (contour-wipe): {percent}%'),
    'wipe_done': ('  contour-wipe hoàn tất: {frames} khung hình', '  contour-wipe complete: {frames} frames'),
    'streams': ('  Luồng nét: {count}, ô mực: {cells}', '  Ink streams: {count}, ink cells: {cells}'),
    'phases': ('  Thời lượng: {ms}ms -> vẽ {ink}f / tô màu {color}f / giữ hình {gaze}f (trọng số {ratio})', '  Duration: {ms}ms -> ink {ink}f / color {color}f / gaze {gaze}f (weights {ratio})'),
    'elapsed': ('  Thời gian kết xuất: {seconds:.1f}s', '  Render time: {seconds:.1f}s'),
    'transcoded': ('  Đã chuyển mã H.264 ({backend}): {path}', '  H.264 transcoding complete ({backend}): {path}'),
    'transcode_failed': ('  [warn] Chuyển mã {backend} thất bại: {error}', '  [warn] {backend} transcoding failed: {error}'),
    'keep_mp4v': ('  [warn] Không có ffmpeg và PyAV; giữ mã hóa mp4v: {path}', '  [warn] Neither ffmpeg nor PyAV available; keeping mp4v: {path}'),
    'h264_hint': ('         Để dùng H.264: pip install av hoặc cài ffmpeg', '         For H.264: pip install av or install ffmpeg'),
    'renderer': ('Bộ kết xuất hoạt hình nét vẽ liên tục', 'Continuous-stroke animation renderer'),
    'read_image': ('[err] Không đọc được ảnh: {path}', '[err] Cannot read image: {path}'),
    'input': ('  Đầu vào: {path}', '  Input: {path}'),
    'dimensions': ('  Kích thước đầu ra: {w}x{h}, tốc độ khung hình: {fps}', '  Output size: {w}x{h}, frame rate: {fps}'),
    'final': ('\nVideo cuối cùng: {path}', '\nFinal video: {path}'),
    'size': ('  Dung lượng tệp: {size:.2f} MB', '  File size: {size:.2f} MB'),
    'done': ('Hoàn tất', 'Done'),
    'writer': ('Không mở được bộ ghi video', 'Cannot open video writer'),
    'read_annotation': ('[err] Không đọc được chú thích: {error}', '[err] Cannot read annotation: {error}'),
    'no_elements': ('[err] Chú thích không có elements', '[err] Annotation contains no elements'),
    'regions': ('  Số vùng: {count}, tổng thời lượng: {ms}ms, đường nét: {ink}, tô màu: {color}', '  Regions: {count}, duration: {ms}ms, ink path: {ink}, color: {color}'),
    'left-to-right': ('trái sang phải', 'left to right'),
    'right-to-left': ('phải sang trái', 'right to left'),
    'top-to-bottom': ('trên xuống dưới', 'top to bottom'),
    'bottom-to-top': ('dưới lên trên', 'bottom to top'),
    'center-out': ('từ tâm ra ngoài', 'center outward'),
}
CATALOGS = {lang: {key: pair[i] for key, pair in MESSAGES.items()}
            for i, lang in enumerate(('vi', 'en'))}
_language = 'vi'


def t(key: str, **values) -> str:
    message = CATALOGS[_language].get(key, key)
    return message.format(**values) if values else message


_ARGPARSE_VI = {
    'usage: ': 'cách dùng: ', 'positional arguments': 'tham số vị trí',
    'options': 'tùy chọn', 'optional arguments': 'tham số tùy chọn',
    'show this help message and exit': 'hiển thị trợ giúp này rồi thoát',
    '%(prog)s: error: %(message)s\n': '%(prog)s: lỗi: %(message)s\n',
    'the following arguments are required: %s': 'các tham số bắt buộc: %s',
    'unrecognized arguments: %s': 'tham số không nhận diện được: %s',
    'argument %s: %s': 'tham số %s: %s',
    'invalid choice: %(value)r (choose from %(choices)s)': 'giá trị không hợp lệ: %(value)r (chọn trong %(choices)s)',
    'invalid %(type)s value: %(value)r': 'giá trị %(type)s không hợp lệ: %(value)r',
    'expected one argument': 'cần một giá trị',
    'expected at least one argument': 'cần ít nhất một giá trị',
    'ignored explicit argument %r': 'giá trị tường minh không được chấp nhận %r',
}


def _argparse_text(message):
    return _ARGPARSE_VI.get(message, message) if _language == 'vi' else message


def configure_streams():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, 'reconfigure', None)
        if reconfigure is not None:
            try:
                reconfigure(encoding='utf-8', errors='backslashreplace')
            except (ValueError, OSError):
                pass  # Captured/closed streams may not support reconfiguration.


def init_cli(argv=None):
    """Preselect language before argparse constructs help or diagnoses errors."""
    global _language
    configure_streams()
    args = list(sys.argv[1:] if argv is None else argv)
    _language = 'vi'
    for index, arg in enumerate(args):
        if arg == '--':
            break
        value = arg.partition('=')[2] if arg.startswith('--lang=') else (
            args[index + 1] if arg == '--lang' and index + 1 < len(args) else None)
        if value in CATALOGS:
            _language = value
    # argparse's gettext hook is shared so nested parsers use the same context.
    argparse._ = _argparse_text


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, argv=None, **kwargs):
        init_cli(argv)
        if 'description' in kwargs:
            kwargs['description'] = t(kwargs['description'])
        kwargs.setdefault('allow_abbrev', False)
        super().__init__(*args, **kwargs)
        self.add_argument('--lang', choices=('vi', 'en'), default=_language, help=t('lang'))

    def add_argument(self, *args, **kwargs):
        if kwargs.get('help'):
            kwargs['help'] = t(kwargs['help'])
        return super().add_argument(*args, **kwargs)


def run_cli(main):
    """Keep expected input/dependency failures readable without swallowing bugs."""
    init_cli()
    try:
        return main()
    except UnicodeError as error:
        print(t('unicode', error=error), file=sys.stderr)
    except ImportError as error:
        print(t('dependency', error=error), file=sys.stderr)
    except (OSError, ValueError, RuntimeError) as error:
        print(t('failure', error=error), file=sys.stderr)
    return 1
