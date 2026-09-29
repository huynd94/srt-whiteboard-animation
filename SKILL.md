---
name: srt-whiteboard-animation
description: Dùng khi người dùng cung cấp phụ đề SRT và yêu cầu tạo video vẽ tay trên bảng trắng, hoạt ảnh nét vẽ liên tục, hoặc phân cảnh minh họa theo phụ đề (SRT whiteboard animation).
---

# Hoạt ảnh bảng trắng từ SRT (điều phối mask + nét vẽ stream)

Chuyển phụ đề SRT thành hoạt ảnh vẽ tay trên bảng trắng: **điều phối** bằng mặt nạ từng vùng (hiện từng vùng theo mạch kể chuyện, ẩn hoàn toàn vùng chưa bắt đầu, bảo vệ phần chồng lấp bằng `protectedRegions`); **cách vẽ** dùng nét liên tục — trong mặt nạ cho phép của mỗi vùng, đầu bút trượt liên tục theo đường khung xương/lưới để đặt mực (`ink` → tô màu `color`). Mọi vùng dùng chung một canvas duy trì trạng thái; vùng đã vẽ được giữ lại.

**Ngôn ngữ:** mặc định dùng tiếng Việt có dấu (`vi`) cho mọi giải thích, phân cảnh, mô tả cấu hình và giao diện hướng tới người dùng. Chỉ dùng tiếng Anh (`en`) khi người dùng yêu cầu rõ ràng. Các mô tả được tạo mới như `storyBasis`, `label`, `narrativeRole` dùng ngôn ngữ đã chọn. Giữ nguyên phụ đề từ nguồn SRT, kể cả trường `subtitle`; không tự dịch phụ đề khi đổi ngôn ngữ. Giữ nguyên tên khóa JSON, định danh kỹ thuật, đường dẫn, mã lệnh và ví dụ gốc. Truyền `--lang vi` hoặc `--lang en` tương ứng khi chạy script; lựa chọn giao diện xem trước độc lập với lựa chọn CLI.

Nét vẽ của skill này **liên tục, liền mạch**, khác với nhảy từng khung hình hay quét xóa hình chữ nhật. Thay vì vẽ stream toàn ảnh một lượt, skill vẽ lần lượt theo **vùng ngữ nghĩa của phụ đề**, cho phép kiểm soát thứ tự và thời điểm xuất hiện của từng thành phần.

## Tham số triển khai mặc định

| Hạng mục | Yêu cầu mặc định |
|---|---|
| Nền giấy | Ảnh sinh ra dùng màu giấy cũ be vàng ấm (khuyến nghị `#F5EBD7`); khi render, lấy mẫu phía trong bốn góc ảnh gốc để tô nền, cấm nền trắng thuần. |
| Cách vẽ | Nét stream liên tục trong từng vùng: `ink` (vẽ nét) → `color` (khôi phục màu gốc); tỷ trọng `ink:color = 2:1`. |
| Đường bút | `--ink-path grid` (lưới, mặc định, ổn định) hoặc `skeleton` (bám khung xương, sát nét hơn với minh họa có nét rõ). |
| Cách tô màu | `--color-fill contour-wipe` (quét theo đường viền, mặc định) hoặc `brush` (tô theo quỹ đạo). |
| Vùng chưa vẽ | Mặt nạ cho phép = hình chữ nhật `region` trừ các vùng phía sau và `protectedRegions`; vùng chưa bắt đầu phải ẩn hoàn toàn. |
| Nguồn thời lượng | `sceneDurationMs` của mỗi ảnh lấy từ khoảng thời gian phụ đề của cảnh đó (khuyến nghị 25–35 giây/cảnh). |
| Khung chỉnh sửa | Mặc định trình xem trước hiển thị tất cả khung chỉnh sửa có đánh số; các khung không thuộc nội dung hoạt ảnh. |

## Quy chuẩn hình ảnh thống nhất (bắt buộc)

Ảnh nguồn của mọi cảnh phải dùng cùng một ngôn ngữ thị giác. Trước khi sinh ảnh, đưa đầy đủ các yêu cầu sau vào prompt; sau khi sinh, kiểm tra từng yêu cầu:

- **Phong cách và bố cục:** minh họa vẽ tay tối giản, phác thảo thuần nét, nét nguệch ngoạc tiết chế kiểu Notion. Ưu tiên diễn đạt khái niệm, không chạy theo tả thực; bố cục đơn giản, nền sạch, nhiều khoảng trống, cảm giác bình hòa và rõ ràng; nét vẽ/nhân vật/bảng màu nhất quán trong cả loạt.
- **Màu sắc và chất liệu:** nền giấy be `#F5EBD7`, nét phác thảo xám đậm; chỉ dùng đỏ, cam, xanh dương làm điểm nhấn khái niệm với lượng nhỏ. Không dùng màu nhấn khác, phối màu bão hòa cao hoặc họa tiết phức tạp.
- **Nhân vật và đối tượng:** diễn đạt bằng đường bao đơn giản, ít nét và khoảng trống; nhấn mạnh quan hệ/thay đổi/khái niệm cốt lõi thay vì tỷ lệ, chất liệu hay chi tiết tả thực.
- **Tuyệt đối cấm:** mọi chữ, từ, ký tự, số, phông chữ hoặc nhãn trong ảnh nguồn của cảnh; cảm giác tả thực, chi tiết nhiếp ảnh, hiệu ứng 3D, chất liệu hội họa; cảnh phức tạp, nền dày đặc, trang trí rườm rà và hình ảnh bão hòa cao.
- **Ngoại lệ cho bàn tay vẽ:** nếu người dùng xác nhận rõ chữ trên thân bút là dấu nhận diện của họ và yêu cầu giữ lại, được giữ dấu đó trong `drawing-hand.png`; đây không phải chữ trong ảnh nguồn của cảnh và không cần xóa hoặc vẽ lại. Khi chưa có xác nhận rõ ràng này, vẫn áp dụng yêu cầu hình ảnh không chữ.

## Các bước chờ xác nhận (bắt buộc)

Trong workflow mặc định, **sau mỗi bước phải dừng và chờ người dùng xác nhận rõ ràng** mới được bắt đầu bước tiếp theo. Trước xác nhận, không được tạo ảnh, chú thích, bản xem trước, video hoặc tệp ghép của bước sau. Không được coi “chưa trả lời”, “đã cho phép chung trước đó” hay “không phản đối” là xác nhận. Nếu người dùng yêu cầu sửa bước trước, chỉ làm lại bước đó, rồi tiếp tục dừng chờ xác nhận.

Thao tác đi kèm duy nhất: **ngay khi tạo xong JSON chú thích, phải tự động mở trình xem trước và nạp thư mục chứa JSON đó**. Đây là phần bàn giao của bước 3, không cần chờ xác nhận riêng để mở trình xem trước. Nếu File System Access API của trình duyệt yêu cầu thao tác người dùng, dùng giao diện trình duyệt để chọn đúng thư mục đã xác định; không vì vậy mà xin thêm xác nhận hoặc chuyển sang yêu cầu người dùng tự mở trình xem trước.

## Workflow

1. **Đọc phụ đề, lập phương án (chưa sinh ảnh).** Dùng `scripts/parse_srt.py` để phân tích SRT thành các mục phụ đề và đề xuất phân cảnh 25–35 giây/cảnh. Từ đó trình bày phương án minh họa: mã cảnh, ý chính, chủ thể hình ảnh, khoảng phụ đề tương ứng và `sceneDurationMs` của mỗi cảnh. Mỗi cảnh chỉ diễn đạt một ý cốt lõi. **Hoàn tất thì dừng, chờ người dùng xác nhận phương án.**
2. **Sinh ảnh nét.** Chỉ sau khi người dùng xác nhận phương án, sinh từng ảnh nét tỷ lệ 16:9 trên nền giấy cũ be vàng ấm `#F5EBD7` theo “Quy chuẩn hình ảnh thống nhất”. Chừa đủ khoảng trống giữa các chủ thể để dễ tự động tách vùng; không sinh chữ, ảnh chụp phức tạp, đối tượng chồng lấp hoặc thành phần trái quy chuẩn. **Hoàn tất thì dừng, trình bày ảnh nét và chờ người dùng xác nhận.**
3. **Đọc phụ đề trước, xem ảnh sau, rồi chú thích và mở trình xem trước.** Chỉ sau khi người dùng xác nhận ảnh nét, đọc phụ đề tương ứng, thực sự xem ảnh và lấy chiều rộng/cao ảnh gốc theo pixel. Không suy đoán hình ảnh chỉ từ phụ đề, không máy móc sắp thứ tự chỉ theo vị trí trên ảnh. Trích các sự kiện trong mạch kể, đối chiếu chủ thể nhìn thấy với sự kiện, rồi sắp thứ tự vẽ theo ngữ nghĩa “thiết lập bối cảnh → nhân vật/vật thể chính → hành động xung đột hoặc thay đổi → phản ứng/kết quả”. Tạo `<ten-anh>.annotation.json`. Ngay khi tạo xong, mở `assets/preview.html` bằng trình duyệt mặc định và dùng chức năng mở thư mục để nạp toàn bộ cặp `<ten>.png` + `<ten>.annotation.json` trong **thư mục chứa tệp chú thích đó**; không được chỉ đưa đường dẫn hoặc yêu cầu người dùng tự thao tác. **Sau khi trình xem trước đã nạp thư mục, dừng và chờ người dùng xác nhận chú thích cùng nội dung xem trước.**
4. **Tạo ảnh kiểm tra vùng.** Chỉ sau khi người dùng xác nhận chú thích và nội dung xem trước, dùng `render_annotation_preview.py` để tạo ảnh kiểm tra số thứ tự/hướng vẽ; đối chiếu phân vùng với mạch kể, bảo đảm mọi vùng nằm trong canvas và các chủ thể chồng lấp được bảo vệ bằng `protectedRegions`. **Hoàn tất thì dừng, chờ người dùng xác nhận ảnh kiểm tra.**
5. **Điều chỉnh trong trình xem trước và lưu.** Chỉ sau khi người dùng xác nhận ảnh kiểm tra, chỉnh trong trình xem trước đã mở và đã nạp đúng thư mục. Mặc định khi chưa phát, hiển thị ảnh đầy đủ và khung vùng. Canvas là **mô phỏng bằng hình chữ nhật**: kéo bốn cạnh/bốn góc để sửa `region`; ở bên phải sửa tên/hướng/**bắt đầu (ms)/kết thúc (ms)** (thời lượng = kết thúc − bắt đầu, chỉ đọc) và **phụ đề**; kéo danh sách thành phần để **đổi thứ tự** (tự đánh lại `sequence`); chọn thành phần sẽ tự tô sáng phụ đề tương ứng. Kéo thanh thời gian hoặc nhấn phát để xem quá trình hiện hình (vùng chưa bắt đầu không hiển thị); `direction` chỉ tác động đến mô phỏng này. Sau khi sửa, chọn chức năng lưu cảnh hiện tại/lưu tất cả để ghi lại `.annotation.json` gốc (gồm `subtitle` của mỗi vùng và căn `sceneDurationMs` về thời điểm kết thúc vùng cuối + 0,5 giây). **Lưu xong thì dừng, chờ người dùng xác nhận chú thích và thời gian cuối cùng.**
6. **Render thành phẩm bằng dòng lệnh.** Chỉ sau khi người dùng xác nhận chú thích và thời gian cuối cùng, dùng `render_stream_whiteboard.py` để xuất MP4 từng cảnh ở chất lượng đầy đủ; kiểm tra ba thời điểm: mở đầu, giữa một thành phần chồng lấp bất kỳ và kết thúc. **Hoàn tất thì dừng, chờ người dùng xác nhận thành phẩm.**
7. **Ghép nhiều cảnh (chỉ áp dụng cho dự án nhiều cảnh).** Chỉ sau khi người dùng xác nhận tất cả thành phẩm từng cảnh, dùng `merge_scenes.py` ghép đúng thứ tự thành một video. **Hoàn tất thì dừng, chờ người dùng xác nhận video tổng hợp cuối cùng.**

## Quy ước thư mục

Tạo trong dự án của người dùng:

```text
assets/whiteboard/<ten-du-an>/
  scene-01-<ten>.png
  scene-01-<ten>.annotation.json     # Cùng tên cơ sở với PNG
  scene-01-<ten>-whiteboard.mp4      # Thành phẩm
  scene-01-<ten>-preview.mp4         # Đoạn render thực, độ phân giải thấp từ trình xem trước
```

Ảnh và cấu hình phải cùng tên cơ sở: `foo.png` đi với `foo.annotation.json`. Trình xem trước dựa vào quy ước này để tự nạp cấu hình.

## Thứ tự ngữ nghĩa và chú thích theo pixel (bắt buộc)

1. **Căn cứ đầu vào:** trước khi chú thích, phải có cả phụ đề và ảnh gốc đã thực sự xem. Thiếu một trong hai thì yêu cầu bổ sung trước, không được tạo chú thích.
2. **Căn cứ thứ tự:** `sequence`, `startMs` và `label` phải phản ánh trình tự sự kiện trong phụ đề, không chỉ dựa vào trái sang phải, trên xuống dưới hay độ nổi bật thị giác.
3. **Căn cứ tọa độ:** mỗi thành phần phải có `x`, `y`, `width`, `height` là số nguyên pixel trong hệ tọa độ ảnh gốc; gốc ở góc trên trái. Cấm dùng phần trăm/tỷ lệ/tọa độ ước lượng hoặc bỏ kích thước. `canvas.width`/`canvas.height` phải bằng kích thước pixel ảnh gốc.
4. **Trường của thành phần:** mỗi phần tử có `sequence`, `narrativeRole`, `subtitle`, `region`, `reveal`, `handPath`. `narrativeRole` mô tả vai trò trong mạch phụ đề bằng ngôn ngữ đã chọn (mặc định tiếng Việt, tiếng Anh khi được yêu cầu); `subtitle` lưu nguyên văn đoạn phụ đề từ SRT tương ứng với vùng, phục vụ liên kết trong trình xem trước và các mục đích sau này. `sequence` liên tục từ 1.
5. **Kiểm tra:** trước khi tạo bản xem trước, kiểm tra từng vùng nằm trong canvas, bao phủ đúng chủ thể nhìn thấy và khớp sự kiện phụ đề; dùng `protectedRegions` bảo vệ các thành phần sẽ vẽ sau khi chủ thể chồng lấp.

## Mô hình thời gian (dành cho nét stream)

- **Tổng thời lượng mỗi cảnh:** `sceneDurationMs` lấy từ khoảng thời gian phụ đề của cảnh (`scenes[].sceneDurationMs` do `parse_srt.py` tạo).
- **Vẽ các vùng nối tiếp:** stream chỉ có một bút chuyển động; các vùng cùng cảnh phải **lần lượt theo thời gian**, không chồng lịch `startMs`. Vùng tiếp theo bắt đầu ở `startMs + durationMs` của vùng trước (có thể cộng khoảng nghỉ 100–300 ms). Nếu lịch `startMs` chồng nhau, renderer vẫn xử lý tuần tự, không vẽ đồng thời về mặt thị giác.
- **Trong vùng, ink→color:** `durationMs` chia thành giai đoạn nét và tô màu theo `ink:color = 2:1`. Thời lượng do **bắt đầu/kết thúc** trong trình xem trước quyết định (kết thúc − bắt đầu), có thể căn theo phụ đề của vùng; cũng có thể dùng mốc 150 pixel/giây × quãng đường vẽ làm ước lượng ban đầu như quy ước gốc.
- **Giữ hình ở cuối:** vẽ xong mọi vùng thì tự bù đến `sceneDurationMs`, đồng thời bảo đảm giữ ảnh gốc đầy đủ ít nhất 0,5 giây ở cuối.
- `reveal.direction` **không quyết định nét vẽ thực** khi dùng stream (nét được sinh tự động từ khung xương/lưới); nó chỉ phục vụ mô phỏng hình chữ nhật của trình xem trước và được giữ để trình xem trước hoạt động.

## Bất biến mặt nạ (tầng điều phối, bắt buộc)

- Tại thời điểm `t`, thành phần chỉ được hiện pixel sau khi `reveal.startMs ≤ t` và không vượt tiến độ vẽ hiện tại. Không được xuất hiện bất kỳ nét, phần tô hoặc hình ảnh nào của thành phần chưa bắt đầu.
- **Mặt nạ cho phép** của mỗi vùng = hình chữ nhật `region` trừ toàn bộ **`region` của các thành phần phía sau**, rồi trừ `reveal.protectedRegions` của chính thành phần đó. Nét stream bị giới hạn trong mặt nạ này, nên vùng phía sau không lộ nét sớm.
- `protectedRegions` dùng số nguyên pixel theo tọa độ ảnh gốc giống `region`; áp dụng khi hình chữ nhật quá lớn, chủ thể chồng lấp hoặc đường nền có thể lộ sớm.
- Renderer đã thực hiện trình tự “chỉ đặt mực trong mặt nạ cho phép → không chạm vào vùng phía sau và vùng bảo vệ”. Mô phỏng hình chữ nhật trong trình xem trước dùng phép trừ `destination-out` tương đương để thể hiện cùng cách điều phối.

## Ví dụ cấu hình gốc

Giữ nguyên ví dụ tiếng Trung dưới đây để bảo toàn dữ liệu minh họa gốc. Với chú thích tạo mới, các mô tả dùng ngôn ngữ đã chọn; `subtitle` luôn giữ nguyên nguồn.

```json
{
  "sceneId": "scene-01",
  "canvas": { "width": 1672, "height": 941 },
  "storyBasis": "该幕字幕的事件摘要",
  "sceneDurationMs": 9000,
  "elements": [
    {
      "id": "rockery",
      "label": "假山场景",
      "sequence": 1,
      "narrativeRole": "故事的场景铺垫",
      "subtitle": "猴子山上，一只小猴子坐在假山顶端，手里拿着香蕉。",
      "type": "structure",
      "region": { "x": 20, "y": 120, "width": 540, "height": 780 },
      "reveal": { "direction": "top_to_bottom", "startMs": 300, "durationMs": 2600, "maskPaddingPx": 22, "protectedRegions": [] },
      "handPath": { "start": [290, 130], "end": [290, 890], "easing": "easeInOut" }
    }
  ]
}
```

> `direction` / `handPath` chỉ dùng trong mô phỏng hình chữ nhật của trình xem trước. Stream tự sinh nét cho thành phẩm; không cần tinh chỉnh hai trường này.

## Sử dụng script và chọn ngôn ngữ

Chạy mọi script render bằng Python trong `.venv` của skill để cô lập phụ thuộc. Các lệnh dưới đây dành cho Windows PowerShell, chạy từ thư mục gốc của skill; thay đường dẫn ví dụ bằng tệp thực tế.

Cả sáu script hỗ trợ `--lang vi` (mặc định) và `--lang en`: `prepare_env.py`, `parse_srt.py`, `render_annotation_preview.py`, `render_stream_whiteboard.py`, `stream_render.py`, `merge_scenes.py`. Cờ này chọn ngôn ngữ thông báo/hướng dẫn CLI và mô tả được sinh, không dịch nội dung nguồn hoặc đổi khóa JSON. Các dấu đầu ra cho máy đọc như `ENV_PY=` và `OUTPUT=` giữ nguyên.

1. **Chuẩn bị môi trường** (lần đầu hoặc khi thiếu phụ thuộc):
   ```powershell
   python scripts/prepare_env.py --check --lang vi
   # Nếu kiểm tra báo thiếu môi trường/phụ thuộc, chạy:
   python scripts/prepare_env.py --lang vi
   ```
   Khi thành công, dòng cuối in `ENV_PY=<duong-dan-python>`. Lệnh chuẩn bị tạo `.venv` và cài phụ thuộc cần thiết, gồm OpenCV, NumPy, PyAV và Pillow. `ENV_PY=...` là đầu ra văn bản, không tự đặt biến PowerShell hay biến môi trường. Gán đường dẫn nhận được rồi gọi bằng toán tử `&`:
   ```powershell
   $ENV_PY = 'D:\Project\srt-whiteboard-animation\.venv\Scripts\python.exe'
   ```
2. **Phân tích phụ đề và đề xuất phân cảnh:**
   ```powershell
   & $ENV_PY scripts/parse_srt.py 'input.srt' --target-sec 30 --min-sec 25 --max-sec 35 --lang vi
   ```
3. **Ảnh kiểm tra vùng có đánh số:**
   ```powershell
   & $ENV_PY scripts/render_annotation_preview.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-regions.png' --lang vi
   ```
4. **Trình xem trước cục bộ (không cần máy chủ):** mở `assets/preview.html` bằng Chrome/Edge, chọn chức năng mở thư mục → nạp mọi ảnh cùng chú thích đồng tên → kéo thả chỉnh sửa → lưu vào tệp gốc. Ghi trực tiếp cần File System Access API (Chrome/Edge); trình duyệt khác tải xuống để thay tệp thủ công. Bộ chọn ngôn ngữ Việt/Anh mặc định là tiếng Việt, lưu lựa chọn trong `localStorage` để dùng lại khi mở trang; không dịch dữ liệu phụ đề hay chú thích đã có. Render vẫn chạy bằng dòng lệnh ở bước kế tiếp.
5. **Render thành phẩm một cảnh:**
   ```powershell
   & $ENV_PY scripts/render_stream_whiteboard.py 'scene-01.png' 'scene-01.annotation.json' 'scene-01-whiteboard.mp4' 'assets/drawing-hand.png' --ink-path grid --color-fill contour-wipe --lang vi
   ```
   Có thể chọn `--ink-path skeleton`, `--color-fill brush` hoặc `--total-ms 9000`. Nếu bỏ `--total-ms`, dùng `sceneDurationMs` trong chú thích. Dòng cuối in `OUTPUT=<duong-dan>`.
6. **Ghép nhiều cảnh:**
   ```powershell
   & $ENV_PY scripts/merge_scenes.py --inputs 'scene-01-whiteboard.mp4' 'scene-02-whiteboard.mp4' 'scene-03-whiteboard.mp4' --output 'final.mp4' --lang vi
   ```

`stream_render.py` là renderer stream toàn ảnh cấp thấp, không thay workflow điều phối vùng đã xác nhận. Khi cần dùng riêng:

```powershell
& $ENV_PY scripts/stream_render.py 'scene-01.png' --out-dir 'out' --total-ms 9000 --lang vi
```

Đầu vào SRT và JSON chú thích dùng UTF-8, chấp nhận cả UTF-8 có BOM (phổ biến với Windows PowerShell 5.1). Phông đi kèm `assets/fonts/NotoSans-Regular.ttf` dùng cho trình duyệt và Pillow để hiển thị tiếng Việt có dấu; giữ nguyên thông tin giấy phép đi kèm phông. Hỗ trợ VI/EN không có nghĩa phông này bao phủ mọi hệ chữ trong phụ đề nguồn.

## Kiểm tra chất lượng

Trước và sau render, xác nhận:

- Khung đầu là nền giấy cũ be vàng ấm sạch, không có nét lộ sớm.
- Đã đọc phụ đề tương ứng và thực sự xem ảnh gốc; `canvas` khớp kích thước pixel ảnh gốc; mọi `region` là tọa độ pixel nguyên và nằm trong canvas.
- `sequence`, `startMs` khớp thứ tự sự kiện phụ đề; số/nhãn/vùng trên ảnh kiểm tra lấy từ cùng một JSON chú thích.
- Kiểm tra ở ba thời điểm: mở đầu, giữa một thành phần chồng lấp bất kỳ và sau khi hoàn tất mọi thành phần. Thành phần chưa vẽ đều vô hình, vùng bảo vệ không lộ nội dung, khung cuối hiển thị toàn bộ ảnh gốc.
- Đầu bút sát nét đang tiến triển; với minh họa nét rõ, có thể dùng `--ink-path skeleton` để bám nét sát hơn.
- Giữ ảnh gốc đầy đủ ít nhất 0,5 giây sau khi mọi thành phần kết thúc.
- Sau khi ghép nhiều cảnh, thứ tự và thời lượng khớp phân cảnh phụ đề.

Nếu cần sửa hiệu ứng, trước hết điều chỉnh và lưu chú thích (vùng/thứ tự/thời gian) trong `assets/preview.html`, rồi render bằng dòng lệnh; không render lặp lại theo phỏng đoán.
