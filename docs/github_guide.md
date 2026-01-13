# Hướng dẫn đưa dự án lên GitHub

Dự án này đã được tối ưu hóa để đưa lên GitHub làm Portfolio. Dưới đây là các bước chi tiết:

## 1. Chuẩn bị (Checklist)
Trước khi push, đảm bảo bạn đã có các file sau (đã được tạo sẵn):
-   [x] `README.md`: Giới thiệu dự án, Tech Stack.
-   [x] `Dockerfile` & `docker-compose.yml`: Cho thấy kỹ năng DevOps.
-   [x] `docs/`: Chứa tài liệu chi tiết (Architecture, Docker Guide, Deploy Guide).
-   [x] `.gitignore`: Đã loại bỏ file rác và data nặng.
-   [x] `requirements.txt`: Danh sách thư viện cần thiết.

## 2. Các bước Push Code

### Bước 1: Khởi tạo Git (Nếu chưa làm)
Chạy lệnh sau tại thư mục gốc của dự án:
```bash
git init
```
*(Nếu đã có folder `.git` ẩn thì bỏ qua bước này)*

### Bước 2: Thêm file vào Staging
```bash
git add .
```

### Bước 3: Commit
Ghi chú thay đổi (Commit message) rõ ràng:
```bash
git commit -m "Initial commit: Quantitative Trading System with Docker & Streamlit Web App"
```

### Bước 4: Kết nối với GitHub Repository
1.  Lên [GitHub](https://github.com/new) tạo một Repository mới (ví dụ: `quantitative-trading-backtest`).
2.  **Không chọn** "Add a README file" (vì mình đã có rồi).
3.  Copy dòng link HTTPS hoặc SSH của repo vừa tạo.
4.  Chạy lệnh kết nối:
    ```bash
    # Thay LINK_GITHUB_CUA_BAN bằng link vừa copy (ví dụ https://github.com/minhnhat215/quant-trading.git)
    git remote add origin LINK_GITHUB_CUA_BAN
    
    # Kiểm tra lại xem đã nhận chưa
    git remote -v
    ```

### Bước 5: Push lên GitHub
```bash
git branch -M main
git push -u origin main
```

## 3. Sau khi Push
*   Vào tab **Settings** của Repo -> **Social preview**: Upload bức ảnh `strategy_comparison.png` lên để làm ảnh đại diện cho dự án cho đẹp.
*   Gắn các **Topic** (thẻ) cho repo: `quantitative-finance`, `backtesting`, `python`, `docker`, `streamlit`, `machine-learning`.
*   Ghim (Pin) repo này lên trang cá nhân của bạn.

## 4. Xử lý lỗi thường gặp
*   **Lỗi "remote origin already exists"**:
    *   Chạy: `git remote remove origin`
    *   Sau đó làm lại bước `git remote add ...`
*   **Lỗi xác thực (Authentication failed)**:
    *   Hãy đảm bảo bạn đã đăng nhập GitHub trên máy, hoặc dùng SSH Key.
