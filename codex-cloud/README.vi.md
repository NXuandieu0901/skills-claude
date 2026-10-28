# Bộ skill Anthropic chọn lọc cho Codex Cloud

Ngày rà soát: 28/10/2026. Nguồn được chốt tại commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44` của NXuandieu0901/skills-claude.

## Trạng thái

Đã chuẩn bị 5 skill trong `.agents/skills/anthropic-*`, sửa chỉ dẫn phụ thuộc Claude, giữ tài nguyên và thông báo giấy phép. Chưa chạy kiểm chứng trên Codex Cloud của tài khoản. Phiên chuẩn bị này là Windows desktop; các kết quả kiểm tra kèm theo chỉ xác nhận gói và phần chạy thử được nêu.

Không thay đổi cài đặt skill cá nhân trên máy Windows. Không ghi vào home của một task cloud và coi đó là cài đặt global. PR nháp/nhánh Git lưu nội dung lâu dài, nhưng chỉ các tác vụ checkout nhánh có nội dung này mới sử dụng được.

## Lựa chọn

| Skill nguồn | Quyết định | Lý do / điều kiện |
|---|---|---|
| frontend-design | Có trong gói | Hướng dẫn thiết kế và xây giao diện, ít phụ thuộc host |
| doc-coauthoring | Có trong gói | Quy trình soạn tài liệu; sửa công cụ tạo file, connector và kiểm tra người đọc; ghi pending khi chưa kiểm thử độc lập |
| internal-comms | Có trong gói | Mẫu giao tiếp nội bộ; thông tin công ty do người dùng cung cấp |
| webapp-testing | Có trong gói | Playwright; cần Python, Chromium, ứng dụng thử; sửa đường dẫn `/mnt/user-data/outputs` |
| slack-gif-creator | Có trong gói | Tạo GIF offline bằng Pillow, numpy, imageio; không cần kết nối Slack |
| algorithmic-art | Để bổ sung khi cần | Có template p5.js; phụ thuộc CDN và chỉ dẫn giữ thương hiệu Anthropic |
| canvas-design | Để bổ sung khi cần | Có font/tài nguyên, cần môi trường render ảnh/PDF |
| theme-factory | Để bổ sung khi cần | Cần xem trước PDF và quy trình chọn theme |
| brand-guidelines | Để bổ sung khi cần | Chuyên cho nhận diện Anthropic; không nên áp dụng mặc định cho thương hiệu của bạn |
| mcp-builder | Để bổ sung khi cần | Hướng dẫn dùng được, nhưng bộ evaluation gọi Anthropic SDK và cần thông tin xác thực riêng |
| pdf, docx, pptx, xlsx | Để bổ sung khi cần | Cần kiểm tra công cụ, font và render theo cloud image; LICENSE riêng, có phần proprietary/source-available. Chưa rà giấy phép để đóng gói/phân phối bốn skill này |
| claude-api | Chưa đưa vào | Chuyên API/SDK Anthropic, trigger rộng; không phải tài liệu API Codex |
| academy-guide | Chưa đưa vào | Chuyên đào tạo sản phẩm Claude |
| discernment-nudge | Chưa đưa vào | Chỉ dẫn hành vi xuyên tác vụ; không cần cho bộ thực dụng ban đầu |
| skill-creator | Chưa đưa vào | Có runner/eval Claude riêng, trùng chức năng skill hệ thống Codex |
| web-artifacts-builder | Chưa đưa vào | Luồng artifact Claude và cài dependency cần rà riêng |

Repository có 19 skill trong `skills/`, cùng `template/SKILL.md` là mẫu. `.claude-plugin/marketplace.json` là manifest marketplace Claude, không phải cấu hình cài toàn tài khoản Codex Cloud. Các skill dùng định dạng Agent Skills tương đồng; điều đó không bảo đảm công cụ, đường dẫn, API hay runtime tương thích hoàn toàn. Bộ chọn lọc dùng tên `anthropic-*` để tránh nhầm với skill hệ thống.

## Dùng bền vững trên Codex Cloud

### Một repository, nhiều thiết bị/tác vụ

1. Xem PR nháp, merge khi chấp nhận. Hoặc chọn trực tiếp nhánh PR khi tạo task thử.
2. Trên web Codex Cloud, cấp quyền GitHub cho repository này và chọn môi trường của repository. Tên menu có thể thay đổi theo phiên bản tài khoản.
3. Tạo task mới checkout đúng nhánh/commit chứa `.agents/skills`. Không cần setup script cho ba skill chỉ chứa hướng dẫn.
4. Yêu cầu: “Liệt kê các skill anthropic-* tìm thấy, cho biết đường dẫn và đọc anthropic-frontend-design.” Kiểm tra danh mục discovery thực tế, không chỉ sự tồn tại của file.
5. Chạy một task khác trên cùng nhánh, rồi kiểm tra lại từ thiết bị khác bằng cùng tài khoản. Chỉ đánh dấu khả năng dùng lại sau khi task mới tìm và dùng được skill.

Các tác vụ trên nhánh cũ chưa chứa gói không tự có skill. Khi cập nhật, sửa bản thích nghi có kiểm soát, cập nhật manifest hash, xem diff và kiểm thử; nguồn trong `skills/` vẫn giữ nguyên.

### Nhiều repository/môi trường Cloud

Lấy bộ này trong một task cloud, không cần cài gì trên máy cá nhân. Từ thư mục gốc của bộ, chạy:

```bash
python3 codex-cloud/manage.py
python3 codex-cloud/manage.py --target-repo /workspace/YOUR_REPOSITORY
python3 codex-cloud/manage.py --target-repo /workspace/YOUR_REPOSITORY --apply
```

Thay đường dẫn bằng root repository thực tế. Lệnh thứ hai là dry-run. Bộ cài chỉ thêm file thiếu, bỏ qua file giống hệt và từ chối ghi đè nội dung khác. Commit thư mục `.agents/skills/anthropic-*` trong repository đích để tác vụ sau checkout lại được. Kèm thông báo giấy phép `codex-cloud/THIRD_PARTY_NOTICES.md` và `codex-cloud/SOURCE-README.md` khi phân phối bản sao; doc-coauthoring không có LICENSE riêng ở snapshot nguồn nên đặc biệt cần giữ thông báo gốc.

Cách này không cần mạng tải skill mỗi lần task chạy. Repo template chứa sẵn bộ là phương án cho dự án mới. Với số lượng repo lớn có thể tự động đồng bộ theo commit cố định; mỗi repo vẫn cần tích hợp, review và kiểm tra discovery. Không có bằng chứng rằng cấu hình một môi trường tự lan sang mọi môi trường khác.

### Dependency khi thực sự dùng web/GIF

Trong phần setup của môi trường Cloud phù hợp, cài các gói cần cho nhiệm vụ. Ví dụ cho Python 3.10+:

```bash
python3 -m pip install playwright pillow imageio numpy
python3 -m playwright install --with-deps chromium
```

Đây là ví dụ bootstrap, chưa phải lockfile tái lập version runtime. Với dự án sản xuất hãy pin dependency trong lockfile của dự án sau khi thử trên cloud image. Chỉ chạy phần cần thiết. Setup có mạng theo tài liệu Cloud; agent phase có thể không có mạng. Nếu thiếu quyền cài thư viện hệ thống, dùng image/môi trường hỗ trợ Chromium hoặc để browser test pending.

Setup/maintenance script được lưu trong cấu hình môi trường có thể tái tạo dependency qua nhiều task; cache container chỉ là tối ưu tạm thời, không phải kho cài dùng chung lâu dài. Khi thay dependency hoặc nhánh gói, kiểm tra maintenance/reset cache theo cấu hình môi trường.

## Cài chung toàn tài khoản

Tài liệu hiện tại mô tả plugin là đường phân phối skill dùng lại ngoài một repo, nhưng điều đó không tự xác nhận plugin cá nhân sẽ được nạp trong Codex Cloud legacy. Phiên này không có công cụ đọc/ghi cài đặt môi trường Cloud, entitlement hay chính sách workspace của tài khoản, nên chưa xác định tài khoản hỗ trợ cài global cloud hay không.

Nếu tài khoản/workspace có danh mục plugin hỗ trợ đúng bề mặt Cloud bạn dùng: cần kiểm tra quyền cài plugin riêng và kiểm chứng bằng task mới trên hai repo. Bộ này chưa được đóng gói/upload thành plugin, và không có khai báo đã cài global. Nếu không có tính năng đó, dùng `.agents/skills` theo repo và repo template; không có bước cài home nào thay thế được thiết lập account-wide.

## Kiểm tra cần hoàn tất trên tài khoản

- Merge/chọn nhánh chứa gói và cấp quyền repository cho Codex Cloud.
- Cài dependency trong môi trường khi cần web/GIF.
- Xác nhận discovery và gọi skill trong task Cloud mới.
- Chạy browser test thực tế; kết quả Windows không chứng minh Chromium hoạt động trong cloud.
- Mở task thứ hai sau khi tạo môi trường mới/reset cache để chứng minh tái tạo không dựa vào home cũ.
- Muốn dùng trên nhiều repo: tích hợp gói vào từng repo, hoặc xác minh giải pháp plugin toàn workspace nếu thực tế có hỗ trợ.

## Nguồn tài liệu đã đọc

- https://github.com/NXuandieu0901/skills-claude/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/environments/cloud-environment
- https://developers.openai.com/plugins/guides/submit-claude-plugin

Đây là rà soát cấu trúc/tính tương thích và kiểm tra gói chọn lọc, không phải audit bảo mật toàn bộ 541 entry của nguồn hoặc thử nghiệm đầy đủ tất cả workflow.
