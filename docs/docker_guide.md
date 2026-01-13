# Docker Guide

Tài liệu này hướng dẫn cách build và chạy project bằng Docker. Việc sử dụng Docker giúp đảm bảo môi trường chạy code đồng nhất, tránh lỗi "it works on my machine".

## 1. Cài đặt Docker
Đảm bảo bạn đã cài đặt Docker Desktop trên máy tính.

## 2. Build Docker Image
Mở terminal tại thư mục gốc của project (nơi chứa file `Dockerfile`) và chạy lệnh:

```bash
docker build -t quant-trading-app .
```

*   `-t quant-trading-app`: Đặt tên cho image là `quant-trading-app`.
*   `.`: Dấu chấm biểu thị build từ thư mục hiện tại.

## 3. Run Container
Sau khi build xong, chạy lệnh sau để khởi chạy ứng dụng:

```bash
docker run --rm -v ${PWD}/data:/app/data quant-trading-app
```

*   `--rm`: Tự động xóa container sau khi chạy xong để tiết kiệm tài nguyên.
*   `-v ${PWD}/data:/app/data`: (Optional) Mount thư mục `data` từ máy thật vào container. Điều này giúp dữ liệu tải về được lưu lại trên máy thật, không bị mất khi tắt container.
    *   *Lưu ý trên Windows Powershell*: Dùng `${PWD}`.
    *   *Lưu ý trên CMD*: Dùng `%cd%`.

## 4. Chạy nhanh với Docker Compose (Khuyên dùng)
Thay vì gõ lệnh dài dòng, bạn chỉ cần một lệnh duy nhất để Build và Run:

```bash
docker-compose up --build
```
*   Tự động build image.
*   Tự động mount thư mục `data`.
*   Chạy ứng dụng.

## 5. Push lên Docker Hub
Để chia sẻ image của bạn lên Docker Hub (giúp người khác kéo về chạy ngay mà không cần build), làm như sau:

### Bước 1: Tạo Repository trên Docker Hub
1. Đăng nhập [Docker Hub](https://hub.docker.com/).
2. Chọn **Create Repository**.
3. Đặt tên (ví dụ: `quant-trading-backtest`).

### Bước 2: Login dưới máy local
```bash
docker login
```

### Bước 3: Tag Image
Gán tag cho image của bạn. Nên đặt tag cụ thể (ví dụ `v2`) thay vì `latest` để quản lý phiên bản.

```bash
# Cú pháp: docker tag <TÊN_IMAGE_GỐC> <USERNAME>/<REPO_NAME>:<TAG>
# Ví dụ:
docker tag quant-trading-app:latest minhnhat215/quant-trading-backtest:v2
```

### Bước 4: Push Image
```bash
docker push minhnhat215/quant-trading-backtest:v2
```

## 6. Tại sao cần làm việc này? (Cho CV)
*   **DevOps/CI-CD**: Biết cách đóng gói và phân phối phần mềm qua Container Registry.
*   **Usability**: Người dùng cuối chỉ cần `docker pull` là chạy được ngay, không cần cài Python/Lib phức tạp.

## 7. Troubleshooting (Sửa lỗi thường gặp)

### Lỗi `401 Unauthorized` khi build
Nếu bạn gặp lỗi `failed to fetch oauth token... 401 Unauthorized`, đây là vấn đề do Docker Credential Helper trên Windows.

**Cách khắc phục:**
1.  Mở file cấu hình Docker tại: `C:\Users\<YourUser>\.docker\config.json` (ví dụ `C:\Users\LENOVO\.docker\config.json`).
2.  Tìm dòng `"credsStore": "desktop",` và **xóa nó đi**.
3.  File sau khi sửa nên trông giống như sau:
    ```json
    {
      "auths": {},
      "currentContext": "desktop-linux"
    }
    ```
4.  Lưu file.
5.  **Quan trọng**: Khởi động lại (Restart) **Docker Desktop** để áp dụng thay đổi.
6.  Chạy lại lệnh `docker build`.

### Nếu vẫn không được (Hard Reset)
Nếu cách trên không hiệu quả, bạn hãy làm mới toàn bộ cấu hình Docker:

1.  Tắt Docker Desktop.
2.  Đổi tên thư mục `.docker` thành `.docker_backup`:
    -   Đường dẫn: `C:\Users\<YourUser>\.docker`
    -   Đổi thành: `C:\Users\<YourUser>\.docker_backup`
3.  Bật lại Docker Desktop. Nó sẽ tự tạo ra folder `.docker` mới tinh.
4.  Thử build lại.

## 6. FAQ - Câu hỏi thường gặp

### Q: Tại sao cần `docker-compose.yml`?
**A:** Để "lười" một cách thông minh.
*   Nếu dùng lệnh thường, bạn phải gõ rất dài: `docker run --rm -v ${PWD}/data:/app/data quant-trading-container`.
*   Nếu dùng compose, bạn chỉ cần: `docker-compose up`. Nó lưu lại các thiết lập (mount ổ đĩa, tên container, port...) vào file để bạn không cần nhớ.

### Q: Project đã có folder `data` rồi, sao cần dòng `volumes: - ./data:/app/data`?
**A:** Đây là khái niệm quan trọng nhất của Docker: **Isolation (Sự cô lập)**.
1.  **Container là một máy tính "mù"**: Mặc định, container chạy như một cái hộp đóng kín. Nó **không hề nhìn thấy** các file trên máy tính của bạn (dù folder data đang nằm ngay đó).
2.  **Mount Volume là "trổ cửa sổ"**: Dòng lệnh `volumes` có tác dụng "mở một đường hầm" nối folder `data` trên máy thật vào trong container.
3.  **Lợi ích**:
    *   **Đọc**: Container đọc được data cũ bạn đã tải.
    *   **Ghi**: Nếu code tải thêm data mới, nó sẽ được lưu ngược ra máy thật. Nếu không mount, container tắt đi là data mới tải cũng **mất sạch**.

### Q: Vậy file `Dockerfile` còn tác dụng gì không?
**A:** Cực kỳ quan trọng, không thể thiếu!
*   **Dockerfile là "Công thức nấu ăn" (Recipe)**: Nó quy định "Món ăn" này gồm những gì (Python 3.11, thư viện pandas, numpy...). Nếu không có Dockerfile, máy tính không biết phải cài đặt môi trường như thế nào.
*   **Docker Compose là "Người phục vụ" (Waiter)**: Nó cầm tờ công thức (Dockerfile) đưa cho đầu bếp làm, sau đó bưng ra bàn (chạy container) theo ý khách hàng (mount volume, mở cổng...).
*   **Mối quan hệ**: Trong file `docker-compose.yml` có dòng `build: .` -> Dòng này chính là bảo: "Hãy tìm cái `Dockerfile` ở thư mục này và nấu theo công thức đó đi".

### Q: Sau khi build xong Image thì xóa Dockerfile đi được không?
**A:**
*   **Về mặt kỹ thuật**: Được. Khi đã có Image rồi, bạn chỉ cần cái Image đó để chạy (deploy), không cần Dockerfile nữa.
*   **Về mặt thực tế**: **KHÔNG NÊN**.
    *   Nếu bạn sửa code (`main.py`), bạn cần Dockerfile để build lại Image mới chứa code mới.
    *   Nếu bạn muốn thêm thư viện mới (ví dụ `scipy`), bạn cần sửa Dockerfile/requirements và build lại.
    *   Nếu bạn đẩy code lên GitHub cho người khác dùng, họ cần Dockerfile để tự build trên máy họ.

## 8. Hướng dẫn dành cho Reviewer (Người chấm bài)
Khi bạn gửi bài, bạn có thể hướng dẫn Reviewer chạy ngay Web App của bạn mà không cần cài đặt gì cả:

1.  **Pull Image từ Docker Hub**:
    ```bash
    # Thay <tag> bằng phiên bản mới nhất (ví dụ v2)
    docker pull minhnhat215/quant-trading-backtest:v2
    ```

2.  **Chạy chương trình**:
    Lưu ý: Cần thêm `-p 8501:8501` để mở cổng cho giao diện Web.

    ```bash
    docker run --rm -p 8501:8501 -v ${PWD}/data:/app/data minhnhat215/quant-trading-backtest:v2
    ```

3.  **Xem kết quả**:
    Mở trình duyệt và truy cập: `http://localhost:8501`

## 9. Quy trình thực tế (Real-world Workflow)
Đây là câu trả lời cho câu hỏi: *"Khi nào thì push lên Docker Hub?"* trong các dự án thực tế:

1.  **Không push thủ công**: Trong môi trường chuyên nghiệp, Developer **hiếm khi** gõ lệnh `docker push` từ máy cá nhân.
2.  **Tự động hóa (CI/CD)**: Thay vào đó, họ dùng các hệ thống tự động (như **GitHub Actions**, Jenkins, GitLab CI).
    *   **Khi nào push?**
        *   Khi Code được merge vào nhánh `main` -> Hệ thống tự động Build -> Test -> Push image `latest` lên Docker Hub (cho môi trường Staging/Dev).
        *   Khi tạo **Release** (ví dụ `v1.0`) -> Hệ thống tự động Push image với tag `v1.0` (cho môi trường Production).
3.  **Tại sao?**
    *   **An toàn**: Không lộ mật khẩu Docker Hub trên máy nhân viên.
    *   **Nhất quán**: Đảm bảo Image luôn được build từ code sạch trên GitHub, không bị lẫn code rác từ máy cá nhân.

*(Bạn có thể chém gió phần này khi phỏng vấn để chứng tỏ mình hiểu về quy trình làm phần mềm chuyên nghiệp)*

### Q: Tại sao chỉ cần 1 dòng lệnh `docker run` là Reviewer chạy được luôn?
**A:** Vì dòng lệnh đó thực ra làm 3 việc ngầm:
1.  **Search & Pull**: Docker máy Reviewer thấy chưa có image `minhnhat215/...` -> Tự động lên Docker Hub tải về (giống như tải game về máy).
2.  **Environment Setup**: Image tải về đã có sẵn 100% mọi thứ (Linux, Python, Thư viện, Code của bạn). Reviewer không cần cài đặt bất cứ thứ gì.
3.  **Port Mapping (`-p`)**: Nó mở một cái cổng từ trong container ra ngoài máy thật, để trình duyệt của Reviewer có thể truy cập được.

Đó là lý do người ta gọi là **"Container"** (Công ten nơ) - Bê nguyên thùng đi đâu cũng chạy được.










