# Hướng dẫn Push Code lên GitHub

Dưới đây là các bước để đưa dự án này lên GitHub.

## 1. Chuẩn bị trên GitHub
1. Đăng nhập vào [GitHub](https://github.com).
2. Tạo một Repository mới (New Repository).
   - **Repository name**: `quant-trading-backtest` (hoặc tên tùy thích).
   - **Description**: Quantitative Trading Strategy Backtesting Project.
   - **Public/Private**: Chọn tùy ý.
   - **Lưu ý**: *Không* cần chọn "Add a README file" vì chúng ta đã tạo sẵn ở dưới máy.

## 2. Thiết lập Git tại máy cá nhân (Local)
Mở terminal (PowerShell hoặc CMD) tại thư mục dự án `d:\UIT\Subjects\quantitativeAI\quant_project` và chạy lần lượt các lệnh sau:

### Bước 2.1: Khởi tạo Git
```bash
git init
```

### Bước 2.2: Thêm file vào Staging
```bash
git add .
```
*Lưu ý: File `.gitignore` đã được tạo để loại bỏ các file không cần thiết (như data csv, pycache).*

### Bước 2.3: Commit code
```bash
git commit -m "Initial commit: Quantitative Trading Project structure and logic"
```

### Bước 2.4: Đổi nhánh chính thành main (nếu cần)
```bash
git branch -M main
```

## 3. Liên kết và Push lên GitHub

Thay thế `<URL_REPO_CUA_BAN>` bằng đường dẫn repository bạn vừa tạo (ví dụ: `https://github.com/username/quant-trading-backtest.git`).

```bash
git remote add origin <URL_REPO_CUA_BAN>
git push -u origin main
```

Sau khi chạy lệnh trên, code của bạn sẽ có mặt trên GitHub.

## Các file đã chuẩn bị sẵn cho bạn:
1. **README.md**: Giới thiệu dự án, cách cài đặt và chạy.
2. **.gitignore**: Cấu hình để git bỏ qua các file rác, file data lớn và file ảo hóa.
3. **requirements.txt**: Danh sách thư viện cần thiết.
