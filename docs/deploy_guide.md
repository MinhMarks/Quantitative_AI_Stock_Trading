# Hướng dẫn Deploy Web App (Streamlit)

Bạn đã có một giao diện Web cho dự án nhưng làm sao để gửi cho Reviewer (không phải tech) xem?

## Cách 1: Chạy Docker tại máy (Dành cho Reviewer có Docker)
1.  **Chạy lệnh**:
    ```bash
    docker-compose up --build
    ```
2.  **Mở trình duyệt**: Truy cập `http://localhost:8501`.

## Cách 2: Deploy lên Streamlit Cloud (Miễn phí & Dễ nhất)
Đây là cách tốt nhất để gửi link cho bất kỳ ai xem (kể cả trên điện thoại).

### Bước 1: Push code lên GitHub
Đảm bảo code hiện tại (bao gồm `app.py`, `requirements.txt`) đã nằm trên GitHub.

### Bước 2: Đăng ký Streamlit Cloud
1.  Truy cập [share.streamlit.io](https://share.streamlit.io/).
2.  Đăng nhập bằng tài khoản **GitHub**.

### Bước 3: Deploy
1.  Bấm **"New app"**.
2.  Chọn Repository GitHub của bạn (`quant-trading-backtest`).
3.  Branch: `main`.
4.  Main file path: `app.py`.
5.  Bấm **"Deploy!"**.

Chờ khoảng 2-3 phút, bạn sẽ có một đường link (ví dụ: `https://quant-backtest.streamlit.app`) để gửi cho sếp hoặc reviewer. Họ chỉ việc bấm vào và nghịch, không cần cài gì cả!
