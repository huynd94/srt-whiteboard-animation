// Classic script: also works when preview.html is opened directly via file://.
window.previewI18n = (() => {
  const messages = {
    vi: {
      title: 'Hoạt hình bảng trắng SRT · Trình chỉnh sửa vùng (không cần máy chủ)',
      brand: 'Bảng trắng SRT · Trình chỉnh sửa vùng', open: 'Mở thư mục…',
      previous: 'Cảnh trước', next: 'Cảnh tiếp theo', scene: 'Chọn cảnh', language: 'Ngôn ngữ',
      overlay: 'Khung vùng', save: 'Lưu cảnh này', saveAll: 'Lưu tất cả',
      hint: 'Nhấn <b>Mở thư mục…</b> để chọn thư mục chứa ảnh nét vẽ (gồm các cặp <code>&lt;tên&gt;.png</code> + <code>&lt;tên&gt;.annotation.json</code>).<br><br>Sau khi tải: mặc định hiển thị toàn bộ ảnh và khung vùng; kéo khung để di chuyển, kéo góc/cạnh để đổi kích thước <code>region</code>; dùng bảng bên phải để chỉnh chính xác tọa độ, hướng, <b>thời gian bắt đầu/kết thúc</b> và <b>phụ đề</b>; kéo các mục trong danh sách để <b>đổi thứ tự vẽ</b>. Kéo thanh thời gian hoặc nhấn phát để xem <b>mô phỏng hiện dần theo hình chữ nhật</b> (vùng chưa bắt đầu sẽ bị ẩn).<br><br>Nhấn <b>Lưu cảnh này</b> / <b>Lưu tất cả</b> để ghi lại tệp <code>.annotation.json</code> gốc (kèm phụ đề của từng vùng).<br><span class="muted">Ghi trực tiếp vào tệp gốc cần Chrome / Edge (File System Access API); trình duyệt khác sẽ tải tệp xuống để bạn tự thay thế tệp gốc. Mô phỏng hình chữ nhật chỉ dùng để kiểm tra bố cục/thời gian; để dựng nét vẽ liên tục thực tế, dùng lệnh <code>render_stream_whiteboard.py</code>.</span>',
      modules: 'Các vùng vẽ', reorder: 'Kéo các mục để đổi thứ tự vẽ', add: '＋ Thêm vùng',
      delete: 'Xóa vùng đã chọn', selected: 'Vùng đã chọn', label: 'Tên', x: 'x', y: 'y',
      width: 'Rộng', height: 'Cao', direction: 'Hướng', start: 'Bắt đầu (ms)', end: 'Kết thúc (ms)', duration: 'Thời lượng (ms)',
      top_to_bottom: 'Từ trên xuống', bottom_to_top: 'Từ dưới lên', left_to_right: 'Từ trái sang phải', right_to_left: 'Từ phải sang trái',
      subtitles: 'Phụ đề', subtitlePlaceholder: 'Phụ đề cho vùng này (lưu trong annotation.json)',
      play: 'Phát', pause: 'Tạm dừng', timeline: 'Thanh thời gian', canvas: 'Bản xem trước vùng vẽ',
      openFailed: 'Không thể mở: {error}', invalidJson: 'Bỏ qua {name}: không thể phân tích JSON',
      noImages: 'Không tìm thấy ảnh có tệp annotation.json đi kèm trong thư mục', unannotated: ' (chưa có chú thích)',
      sceneCount: '{count} ảnh ({annotated} ảnh có chú thích)', downloadFallback: 'Trình duyệt này không hỗ trợ ghi trực tiếp; tệp sẽ được tải xuống khi lưu',
      imageFailed: 'Không thể tải ảnh: {name}', elementCount: '{count} vùng', noSubtitle: '(Chưa có phụ đề)',
      newRegion: 'Vùng mới', unsaved: '● Chưa lưu', writeDenied: 'Chưa được cấp quyền ghi', saved: 'Đã lưu: {name}', saveFailed: 'Không thể lưu: {error}',
      seconds: '{value}s', time: '{current}s / {total}s', unknownError: 'Lỗi không xác định'
    },
    en: {
      title: 'SRT Whiteboard Animation · Region Editor (no server required)',
      brand: 'SRT Whiteboard · Region Editor', open: 'Open folder…',
      previous: 'Previous scene', next: 'Next scene', scene: 'Select scene', language: 'Language',
      overlay: 'Region outlines', save: 'Save this scene', saveAll: 'Save all',
      hint: 'Click <b>Open folder…</b> to select the folder containing line art (paired <code>&lt;name&gt;.png</code> + <code>&lt;name&gt;.annotation.json</code> files).<br><br>After loading: the full image and region outlines appear by default. Drag a box to move it or drag its corners/edges to resize its <code>region</code>. Use the right panel to edit coordinates, direction, <b>start/end times</b> and <b>subtitles</b>. Drag list items to <b>change drawing order</b>. Scrub the timeline or press play to preview the <b>rectangular reveal simulation</b> (regions that have not started remain hidden).<br><br>Click <b>Save this scene</b> / <b>Save all</b> to write back to the original <code>.annotation.json</code> files (including each region’s subtitles).<br><span class="muted">Writing to original files requires Chrome / Edge (File System Access API). Other browsers download files for you to replace manually. The rectangular simulation is only for layout/timing checks; use <code>render_stream_whiteboard.py</code> on the command line to render actual continuous strokes.</span>',
      modules: 'Drawing regions', reorder: 'Drag items to change drawing order', add: '＋ Add region',
      delete: 'Delete selected', selected: 'Selected region', label: 'Name', x: 'x', y: 'y',
      width: 'Width', height: 'Height', direction: 'Direction', start: 'Start (ms)', end: 'End (ms)', duration: 'Duration (ms)',
      top_to_bottom: 'Top to bottom', bottom_to_top: 'Bottom to top', left_to_right: 'Left to right', right_to_left: 'Right to left',
      subtitles: 'Subtitles', subtitlePlaceholder: 'Subtitle for this region (saved in annotation.json)',
      play: 'Play', pause: 'Pause', timeline: 'Timeline', canvas: 'Drawing region preview',
      openFailed: 'Could not open: {error}', invalidJson: 'Skipping {name}: JSON parsing failed',
      noImages: 'No images with matching annotation.json files found in this folder', unannotated: ' (not annotated)',
      sceneCount: '{count} images ({annotated} annotated)', downloadFallback: 'This browser cannot write directly; saving will download files instead',
      imageFailed: 'Could not load image: {name}', elementCount: '{count} regions', noSubtitle: '(No subtitle)',
      newRegion: 'New region', unsaved: '● Unsaved', writeDenied: 'Write permission was not granted', saved: 'Saved: {name}', saveFailed: 'Could not save: {error}',
      seconds: '{value}s', time: '{current}s / {total}s', unknownError: 'Unknown error'
    }
  };
  const storageKey = 'srt-whiteboard-language';
  let language = 'vi';
  try { if (localStorage.getItem(storageKey) === 'en') language = 'en'; } catch (_) { /* Storage may be blocked for local files. */ }
  function t(key, values = {}) {
    const text = messages[language][key] ?? messages.vi[key] ?? key;
    return text.replace(/\{(\w+)\}/g, (match, name) => Object.prototype.hasOwnProperty.call(values, name) ? String(values[name]) : match);
  }
  function setLanguage(value) {
    language = value === 'en' ? 'en' : 'vi';
    try { localStorage.setItem(storageKey, language); } catch (_) { /* Keep the in-memory choice. */ }
  }
  function apply(root = document) {
    document.documentElement.lang = language;
    document.title = t('title');
    root.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    root.querySelectorAll('[data-i18n-html]').forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
    for (const attr of ['title', 'aria-label', 'placeholder']) {
      root.querySelectorAll(`[data-i18n-${attr}]`).forEach(el => el.setAttribute(attr, t(el.getAttribute(`data-i18n-${attr}`))));
    }
  }
  return { t, setLanguage, apply, get language() { return language; } };
})();
