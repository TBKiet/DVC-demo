# Tóm Tắt & Giải Thích Các Bước Triển Khai Dự Án "EcoVision"

Dưới đây là tổng hợp những gì tôi đã thực hiện để xây dựng nền móng cho dự án phân loại rác thải của bạn, cùng với lý do "Tại sao" cho từng bước. Mục tiêu là xây dựng một dự án chuẩn kỹ sư AI hiện đại (AI Engineer style) chứ không chỉ là một bài tập notebook đơn thuần.

---

## 1. Khởi tạo Cấu Trúc Dự Án (Project Structure)

**Những gì đã làm:**

- Tạo các thư mục chuẩn: `src/` (mã nguồn), `data/` (dữ liệu), `models/` (lưu model), `notebooks/` (nháp).
- Tạo file `requirements.txt` liệt kê thuvienj.

**Tại sao?**

- **Tiêu chuẩn ngành**: Giúp code gọn gàng, dễ bảo trì và người khác nhìn vào hiểu ngay đâu là code train, đâu là code app.
- **Tránh "Spaghetti code"**: Tách biệt code xử lý dữ liệu (`src/data`) và code huấn luyện (`src/train.py`) giúp dễ debug hơn là viết tất cả trong 1 file.

## 2. Quản lý Dữ Liệu (TrashNet & DVC)

**Những gì đã làm:**

- Tải bộ dữ liệu **TrashNet** (Cardboard, Glass, Metal, Paper, Plastic, Trash).
- Cài đặt **DVC (Data Version Control)** và chạy `dvc init`.
- Thêm folder `data/raw` vào DVC (`dvc add data/raw`).

**Tại sao?**

- **DVC là "Git cho dữ liệu"**: Git không giỏi quản lý file lớn (ảnh, video). Nếu bạn đẩy 2GB ảnh lên GitHub, nó sẽ rất chậm hoặc bị chặn. DVC giúp bạn version control dữ liệu y như code, nhưng lưu trữ thực tế ở nơi khác (S3, GDrive, hoặc local folder bên ngoài git).
- **Reproducibility (Tính tái lập)**: Đảm bảo rằng model X được train trên chính xác version dữ liệu Y.

## 3. Huấn luyện Model (PyTorch & W&B)

**Những gì đã làm:**

- Viết script `src/train.py` sử dụng **PyTorch**.
- Sử dụng **Transfer Learning (ResNet18)** để tận dụng kiến thức từ ImageNet, giúp train nhanh và chính xác hơn với ít dữ liệu.
- Tích hợp **Weights & Biases (W&B)** (`wandb.init`, `wandb.log`).
- **Tối ưu cho Mac**: Thêm logic tự động chọn device `mps` (Metal Performance Shaders) để train nhanh trên chip Apple Silicon.

**Tại sao?**

- **W&B**: Thay vì ngồi nhìn màn hình console chạy text `Loss: 0.5...`, W&B vẽ biểu đồ loss/accuracy theo thời gian thực. Nó giúp bạn so sánh các lần train (experiments) để biết hyperparameter nào tốt nhất.
- **PyTorch**: Framework linh hoạt, standard trong cả nghiên cứu và production.

## 4. Xây dựng Ứng Dụng (Streamlit)

**Những gì đã làm:**

- Viết `src/app.py` tạo giao diện web đơn giản cho phép upload ảnh và dự đoán.
- Loading model đã train và xử lý ảnh (resize, normalize) giống hệt lúc train.

**Tại sao?**

- **Demo nhanh**: Để trình diễn kết quả ("Show, don't just tell"). Một UI trực quan có giá trị thuyết phục cao hơn nhiều so với một file log chạy dòng lệnh.
- **Streamlit**: Cực nhanh để build data app mà không cần biết HTML/CSS/JS.

## 5. Đóng Gói & Triển Khai (Docker & Dockerfile)

**Những gì đã làm:**

- Viết `Dockerfile` định nghĩa môi trường chạy: Python 3.9, cài dependencies, copy code và chạy app.
- Tạo `.dockerignore` để tránh copy rác vào container.

**Tại sao?**

- **"Works on my machine"**: Docker đảm bảo code chạy trên máy bạn cũng sẽ chạy y hệt trên máy chủ, máy đồng nghiệp hay trên cloud (AWS/GCP).
- **Dễ deployment**: Chỉ cần 1 lệnh `docker run` là toàn bộ app (bao gồm môi trường, thư viện) được bật lên.

---

### Tổng kết

Dự án này tuy nhỏ nhưng đã bao gồm đầy đủ vòng đời MLOps cơ bản:
**Data (DVC) ➡️ Training (PyTorch/W&B) ➡️ Packaging (Docker) ➡️ Serving (Streamlit)**.
