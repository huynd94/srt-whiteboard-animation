# Skill hoạt ảnh bảng trắng từ SRT

**Tiếng Việt (mặc định)** | [English](README.en.md)

Chuyển phụ đề SRT thành video vẽ tay trên bảng trắng theo thứ tự kể chuyện. Skill kết hợp **điều phối mặt nạ từng vùng** với **nét vẽ liên tục**: mỗi thành phần xuất hiện theo phụ đề, đầu bút đặt mực liên tục trong vùng rồi tô màu, cuối cùng xuất MP4.

Phù hợp để biến nội dung giải thích kiến thức, lời kể chuyện, phụ đề khóa học hoặc kịch bản video ngắn thành hoạt ảnh vẽ tay trên nền giấy be vàng ấm.

## Ví dụ thành phẩm

**Cảnh: tranh chuối ở núi khỉ** — theo mạch kể của phụ đề, lần lượt vẽ hòn non bộ và khỉ nhỏ, khỉ lớn cướp chuối, rồi các em nhỏ đứng xem. Tên và dữ liệu ví dụ gốc được giữ nguyên.

![Tranh chuối ở núi khỉ: minh họa hoạt ảnh bảng trắng từ SRT](examples/scene-01-monkey-mountain-stream.gif)

Ảnh nét gốc: [xem PNG](examples/scene-01-monkey-mountain.png).

## Tính năng chính

- Phân tích SRT và đề xuất chia cảnh với thời lượng 25–35 giây.
- Trình bày phân cảnh và phương án minh họa trước, mỗi cảnh chỉ diễn đạt một ý cốt lõi.
- Sắp thứ tự vẽ theo sự kiện trong phụ đề thay vì vị trí trên ảnh.
- Quản lý vùng, thời gian, liên kết phụ đề và vùng bảo vệ chồng lấp bằng `annotation.json`.
- Vẽ liên tục từng vùng: `ink` dựng nét trước, `color` tô màu sau.
- Chỉnh vùng, thứ tự, thời gian và liên kết phụ đề bằng trình xem trước trong trình duyệt.
- Render từng cảnh và ghép nhiều cảnh thành MP4 hoàn chỉnh.

## Ngôn ngữ Việt/Anh

Tiếng Việt có dấu là mặc định (`vi`); chỉ dùng tiếng Anh (`en`) khi được yêu cầu rõ ràng. Hướng dẫn, phân cảnh và mô tả tạo mới (`storyBasis`, `label`, `narrativeRole`) theo ngôn ngữ đã chọn. **Phụ đề nguồn và trường `subtitle` luôn giữ nguyên**, không tự dịch khi đổi ngôn ngữ. Khóa JSON, định danh kỹ thuật và ví dụ gốc được giữ nguyên.

Cả sáu script Python đều nhận `--lang vi` hoặc `--lang en` (mặc định `vi`):

| Script | Chức năng |
|---|---|
| `scripts/prepare_env.py` | Kiểm tra/chuẩn bị môi trường Python |
| `scripts/parse_srt.py` | Phân tích phụ đề và đề xuất phân cảnh |
| `scripts/render_annotation_preview.py` | Tạo ảnh kiểm tra chú thích |
| `scripts/render_stream_whiteboard.py` | Render MP4 theo từng vùng chú thích |
| `scripts/stream_render.py` | Renderer stream toàn ảnh cấp thấp |
| `scripts/merge_scenes.py` | Ghép MP4 theo thứ tự |

`--lang` chọn ngôn ngữ thông báo/hướng dẫn CLI và mô tả được sinh; không dịch dữ liệu nguồn hay chú thích đã có. Các dấu đầu ra cho máy đọc như `ENV_PY=` và `OUTPUT=` giữ nguyên.

Trong `assets/preview.html`, chọn Việt/Anh bằng bộ chọn ngôn ngữ. Lựa chọn được lưu trong `localStorage` để dùng lại khi mở trang; lần đầu mặc định là tiếng Việt. Lựa chọn giao diện độc lập với `--lang` của CLI.

SRT và JSON chú thích dùng **UTF-8**, hỗ trợ cả **UTF-8 có BOM** (thường gặp khi lưu bằng Windows PowerShell 5.1). Phông đi kèm `assets/fonts/NotoSans-Regular.ttf` dùng cho trình duyệt và Pillow để hiển thị tiếng Việt có dấu. Giữ nguyên giấy phép đi kèm phông; hỗ trợ VI/EN không bảo đảm phông bao phủ mọi hệ chữ của phụ đề nguồn.

Prompt mặc định:

```text
Dùng $srt-whiteboard-animation tạo hoạt ảnh vẽ tay trên bảng trắng từ phụ đề SRT này. Dùng tiếng Việt cho phần hướng dẫn và mô tả, giữ nguyên phụ đề nguồn và chờ xác nhận sau mỗi bước.
```

Để yêu cầu tiếng Anh rõ ràng:

```text
Use $srt-whiteboard-animation to create a hand-drawn whiteboard animation from this SRT. Use English for guidance and generated descriptions, keep the source subtitles unchanged, and wait for confirmation after each step.
```

## Cách hoạt động

Nguyên tắc chính là **phụ đề dẫn dắt, xác nhận từng bước**. Sau mỗi bước, dừng chờ người dùng xác nhận rõ ràng để tránh tốn công render khi phân cảnh, ảnh nét hoặc chú thích chưa chốt. Quy trình và mọi ràng buộc đầy đủ nằm trong [SKILL.md](SKILL.md).

1. Phân tích SRT, trình bày phân cảnh và phương án minh họa; chờ xác nhận.
2. Sau xác nhận, sinh ảnh nét đồng nhất về phong cách; chờ xác nhận ảnh nét.
3. Sau xác nhận ảnh nét, đọc phụ đề, xem ảnh gốc, tạo chú thích; ngay lập tức mở trình xem trước và nạp thư mục chứa chú thích. Chờ xác nhận chú thích và nội dung xem trước.
4. Sau xác nhận, tạo ảnh kiểm tra phân vùng và hướng; chờ xác nhận ảnh kiểm tra.
5. Sau xác nhận, chỉnh vùng, thứ tự kể chuyện, thời gian và liên kết phụ đề trong trình xem trước, rồi lưu; chờ xác nhận chú thích và thời gian cuối cùng.
6. Sau xác nhận cuối, render MP4 từng cảnh; chờ xác nhận thành phẩm.
7. Với dự án nhiều cảnh, chỉ ghép sau khi mọi thành phẩm từng cảnh được xác nhận; chờ xác nhận video tổng hợp.

Không coi im lặng, cho phép chung trước đó hay không phản đối là xác nhận. Nếu cần sửa bước trước, chỉ làm lại bước đó rồi chờ xác nhận mới. Mở và nạp trình xem trước ngay sau khi tạo JSON là phần bàn giao của bước 3, không phải một bước xin xác nhận riêng.

## Quy chuẩn hình ảnh

- Nền giấy be vàng ấm, khuyến nghị `#F5EBD7`.
- Nét phác thảo xám đậm; đỏ, cam, xanh dương chỉ làm điểm nhấn khái niệm với lượng nhỏ.
- Vẽ tay tối giản, nền sạch và nhiều khoảng trống.
- Không có chữ/nhãn trong ảnh nguồn của cảnh, cảm giác nhiếp ảnh, hiệu ứng 3D hoặc họa tiết phức tạp.

## Cài đặt và môi trường

Skill có script chuẩn bị môi trường Python ảo riêng. Chạy các lệnh sau từ thư mục gốc kho mã bằng **Windows PowerShell**:

```powershell
python scripts/prepare_env.py --check --lang vi
# Nếu kiểm tra báo thiếu môi trường/phụ thuộc, chạy:
python scripts/prepare_env.py --lang vi
```

Khi thành công, dòng cuối in `ENV_PY=<duong-dan-python>`. Dùng đúng trình thông dịch đó cho các lệnh tiếp theo để cô lập phụ thuộc. Script chuẩn bị cài các phụ thuộc cần thiết, gồm OpenCV, NumPy, PyAV và Pillow.

**Lưu ý `ENV_PY`:** đây là dòng văn bản đầu ra, không tự tạo biến PowerShell hoặc biến môi trường. Gán đường dẫn nhận được vào `$ENV_PY`; ví dụ dưới đây cần sửa nếu đặt skill ở nơi khác. Toán tử `&` gọi được cả đường dẫn có dấu cách:

```powershell
$ENV_PY = 'D:\Project\srt-whiteboard-animation\.venv\Scripts\python.exe'
& $ENV_PY scripts/parse_srt.py --help --lang vi
```

## Cấu trúc tài nguyên dự án

```text
assets/whiteboard/<ten-du-an>/
├── scene-01-<ten>.png
├── scene-01-<ten>.annotation.json
├── scene-01-<ten>-whiteboard.mp4
└── scene-01-<ten>-preview.mp4
```

Ảnh và chú thích phải cùng tên cơ sở, ví dụ `scene-01-demo.png` đi với `scene-01-demo.annotation.json`.

## Định dạng chú thích

Mỗi thành phần dùng tọa độ pixel nguyên của ảnh gốc, liên kết với sự kiện phụ đề qua `sequence`, `subtitle` và `narrativeRole`. Sắp vùng theo “thiết lập bối cảnh → nhân vật/vật thể chính → hành động hoặc thay đổi → phản ứng/kết quả”.

Ví dụ gốc dưới đây được giữ nguyên, bao gồm nội dung tiếng Trung. Mô tả tạo mới theo ngôn ngữ đã chọn; phụ đề luôn theo nguồn.

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

`direction` và `handPath` phục vụ mô phỏng hình chữ nhật trong trình xem trước; nét vẽ thực của thành phẩm do renderer stream tự sinh. Khi đối tượng che nhau, khai báo phần cần hiện muộn trong `protectedRegions` của thành phần vẽ trước để tránh lộ sớm nội dung phía sau.

## Các lệnh thường dùng

Thay tên tệp ví dụ bằng đường dẫn thực tế. Các lệnh một dòng dưới đây dùng được trong PowerShell; đổi `--lang vi` thành `--lang en` khi cần tiếng Anh.

Phân tích phụ đề và đề xuất phân cảnh:

```powershell
& $ENV_PY scripts/parse_srt.py 'input.srt' --target-sec 30 --min-sec 25 --max-sec 35 --lang vi
```

Tạo ảnh kiểm tra vùng:

```powershell
& $ENV_PY scripts/render_annotation_preview.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-regions.png' --lang vi
```

Mở `assets/preview.html` bằng Chrome/Edge, dùng chức năng mở thư mục để nạp thư mục cảnh rồi chỉnh vùng, thứ tự, thời gian và liên kết phụ đề. Không cần máy chủ. Ghi trực tiếp vào tệp cần File System Access API; với trình duyệt khác, tải tệp xuống rồi thay bản gốc thủ công.

Render một cảnh:

```powershell
& $ENV_PY scripts/render_stream_whiteboard.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-whiteboard.mp4' 'assets/drawing-hand.png' --ink-path grid --color-fill contour-wipe --lang vi
```

Nếu không truyền `--total-ms`, renderer dùng `sceneDurationMs` từ chú thích; dòng cuối in `OUTPUT=<duong-dan>`.

Renderer stream toàn ảnh cấp thấp (dùng riêng, không thay thế workflow chú thích theo vùng):

```powershell
& $ENV_PY scripts/stream_render.py 'scene-01.png' --out-dir 'out' --total-ms 9000 --lang vi
```

Ghép nhiều cảnh:

```powershell
& $ENV_PY scripts/merge_scenes.py --inputs 'scene-01-whiteboard.mp4' 'scene-02-whiteboard.mp4' 'scene-03-whiteboard.mp4' --output 'final.mp4' --lang vi
```

## Kiểm tra chất lượng

- Khung đầu là nền giấy be vàng ấm sạch, không lộ nét trước thời điểm.
- `canvas` khớp kích thước ảnh gốc; mọi vùng dùng tọa độ pixel nguyên, nằm trong canvas.
- `sequence`, `startMs` khớp mạch kể của phụ đề.
- Ở các khung giữa, vùng chưa bắt đầu và vùng bảo vệ không lộ sớm.
- Đầu bút sát nét stream hiện tại; với ảnh nét rõ, có thể chọn `--ink-path skeleton`.
- Mỗi cảnh giữ ảnh hoàn chỉnh ít nhất 0,5 giây ở cuối; thứ tự ghép nhiều cảnh khớp phân cảnh phụ đề.

## Nội dung kho mã

```text
srt-whiteboard-animation/
├── README.md                         # Tài liệu tiếng Việt (mặc định)
├── README.en.md                      # Tài liệu tiếng Anh tương đương
├── SKILL.md                          # Workflow và ràng buộc có thẩm quyền
├── assets/
│   ├── drawing-hand.png              # Tài nguyên bàn tay vẽ
│   ├── fonts/NotoSans-Regular.ttf    # Phông cho trình duyệt và Pillow
│   └── preview.html                  # Trình xem trước/chỉnh sửa cục bộ
├── examples/                         # Tài nguyên ví dụ gốc của README
├── scripts/
│   ├── parse_srt.py                  # Phân tích phụ đề và đề xuất phân cảnh
│   ├── render_annotation_preview.py  # Ảnh kiểm tra chú thích
│   ├── render_stream_whiteboard.py   # Renderer MP4 theo vùng
│   ├── stream_render.py              # Renderer stream toàn ảnh cấp thấp
│   ├── merge_scenes.py               # Ghép nhiều cảnh
│   └── prepare_env.py                # Chuẩn bị môi trường phụ thuộc
└── agents/openai.yaml                # Metadata Codex, mặc định tiếng Việt
```

## Đóng góp

Hoan nghênh Issue và Pull Request. Mọi thay đổi logic vẽ cần kiểm tra bằng phụ đề, chú thích và video thực tế để xác minh bảo vệ mặt nạ, thời gian và hình ảnh cuối cùng.

## Giấy phép

Dự án mã nguồn mở theo MIT License; xem [LICENSE](LICENSE). Phông đi kèm có giấy phép riêng trong `assets/fonts/`.

## Về tác giả

Giới thiệu và tên tài khoản gốc được giữ nguyên để ghi công chính xác:

一个爱养鱼的老登 / AI Builder / 用 AI 团队打造一人公司。

抖音、B站、公众号：江哥是老登啊

Tạm dịch: một người mê nuôi cá / AI Builder / dùng đội ngũ AI xây dựng công ty một người. Tác giả dùng tên **江哥是老登啊** trên Douyin, Bilibili và tài khoản công chúng WeChat.
