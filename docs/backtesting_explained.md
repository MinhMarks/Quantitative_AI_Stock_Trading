# Cơ chế hoạt động của Backtesting (Backtesting Logic)

Tài liệu này giải thích chi tiết cách thức lớp `Backtester` trong project hoạt động để mô phỏng chiến lược giao dịch trên dữ liệu lịch sử.

## 1. Tổng quan
Backtesting (Kiểm thử quá khứ) là quá trình chạy một chiến lược giao dịch trên dữ liệu lịch sử để đánh giá hiệu quả của nó trước khi áp dụng vào thực tế. Hệ thống của chúng ta sử dụng phương pháp **Event-Driven** (hướng sự kiện) đơn giản hóa, lặp qua từng ngày giao dịch.

## 2. Phân chia dữ liệu (Data Splitting) - CRITICAL

Trong `main.py`, chúng ta áp dụng **Time Series Split** (Chia theo thời gian) thay vì Random Split để tránh lỗi kinh điển **Look-ahead Bias** (Nhìn thấy tương lai).

### Cơ chế chia:
*   **Tổng dữ liệu**: 2015-01-01 đến 2024-01-01 (9 năm).
*   **Training Set (Dữ liệu huấn luyện)**: `2015-01-01` đến `2021-12-31`.
    *   Mục đích: Dùng để "dạy" mô hình Machine Learning (Random Forest) nhận biết xu hướng. Mô hình chỉ được biết thông tin của quá khứ này.
*   **Testing Set (Dữ liệu kiểm thử)**: `2022-01-01` đến `2023-12-31`.
    *   Mục đích: Dùng để Backtest chiến lược và đánh giá hiệu quả.
    *   **Nguyên tắc**: Dữ liệu này **hoàn toàn mới** đối với mô hình, mô phỏng việc bạn trade thực tế từ năm 2022 trở đi.

```python
# Code thực tế trong main.py
train_end_date = '2021-12-31'
test_start_date = '2022-01-01'

train_data = data.loc[:train_end_date] # 2015 -> 2021
test_data = data.loc[test_start_date:] # 2022 -> 2023
```

## 3. Các thành phần chính của Backtester

### 3.1. Khởi tạo (`__init__`)
Khi khởi tạo `Backtester`, chúng ta thiết lập các tham số môi trường:
-   **Initial Capital**: Số vốn ban đầu (ví dụ: $10,000).
-   **Transaction Cost (`transaction_cost_pct`)**: Phí giao dịch cho mỗi lần mua/bán (ví dụ: 0.1% = 0.001).
-   **Slippage (`slippage_pct`)**: Độ trượt giá (ví dụ: 0.05% = 0.0005).

### 3.2. Vòng lặp giao dịch (`run`)
Hàm `run` thực hiện các bước sau:
1.  **Nhận tín hiệu (Signals)**: Lấy chuỗi tín hiệu từ `Strategy` (đã được train trên tập Train nếu là ML).
2.  **Lặp theo ngày (Iterate Daily)**: Duyệt qua từng ngày trong dữ liệu giá (`close`).
3.  **Xử lý tín hiệu**:
    -   Nếu tín hiệu là **1 (Long)** và chưa có vị thế: MUA.
    -   Nếu tín hiệu là **0 (Cash)** và đang giữ cổ phiếu: BÁN.

## 4. Logic Khớp lệnh chi tiết

### 4.1. Mua (Buy Logic)
$$ \text{Giá Mua} = \text{Giá Close} \times (1 + \text{Slippage}) $$
*Tiền mặt giảm = Giá trị lệnh + Phí giao dịch.*

### 4.2. Bán (Sell Logic)
$$ \text{Giá Bán} = \text{Giá Close} \times (1 - \text{Slippage}) $$
*Tiền mặt tăng = Doanh thu - Phí giao dịch.*

## 5. Định giá (Mark-to-Market)
$$ \text{Portfolio Value} = \text{Tiền mặt} + (\text{Số lượng cổ phiếu} \times \text{Giá Close hiện tại}) $$
