# Hướng Dẫn Kết Nối DVC với AWS S3

## Giới Thiệu

DVC (Data Version Control) là công cụ quản lý phiên bản cho dữ liệu và mô hình machine learning. AWS S3 là dịch vụ lưu trữ đám mây phổ biến có thể được sử dụng làm remote storage cho DVC.

### Cách DVC Lưu Trữ Dữ Liệu

> [!IMPORTANT]
> DVC **không lưu trữ file gốc** trên S3. Thay vào đó, DVC sử dụng **content-addressable storage** (lưu trữ theo nội dung).

**Cơ chế hoạt động:**

1. **Hash MD5**: DVC tính hash MD5 của file (ví dụ: `68e3aef104f5a822d8e73bb2e2908d`)
2. **Lưu theo hash**: File được lưu với tên là hash, không có extension
3. **Cấu trúc thư mục**: Sử dụng 2 ký tự đầu của hash làm folder
   ```
   s3://bucket/files/md5/00/68e3aef104f5a822d8e73bb2e2908d
                         ^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         |   hash của file
                         2 ký tự đầu làm folder
   ```

**Ví dụ:**

- File gốc: `data/image.jpg` (1.5 MB)
- Trên S3: `s3://bucket/files/md5/a1/b2c3d4e5f6...` (không có `.jpg`)
- File `.dvc`: `data/image.jpg.dvc` (chứa hash và metadata)

**Lợi ích:**

- ✅ **Deduplication**: File giống nhau chỉ lưu 1 lần
- ✅ **Integrity**: Hash đảm bảo file không bị corrupt
- ✅ **Efficiency**: Tiết kiệm storage và bandwidth

> [!NOTE]
> Để lấy file gốc, **không truy cập trực tiếp S3**. Sử dụng `dvc pull` để DVC tự động restore file về đúng tên và vị trí.

## Yêu Cầu

- Python 3.7 trở lên
- Tài khoản AWS với quyền truy cập S3
- AWS Access Key ID và Secret Access Key

## Bước 1: Cài Đặt DVC

```bash
pip install dvc
pip install dvc-s3
```

> [!NOTE]
> Lệnh `pip install dvc-s3` sẽ tự động cài đặt các dependencies cần thiết như `aiobotocore`, `s3fs`, và `botocore`.

## Bước 2: Cấu Hình AWS Credentials

### Cách 1: Sử dụng AWS CLI

```bash
# Cài đặt AWS CLI
pip install awscli

# Cấu hình credentials
aws configure
```

Nhập thông tin khi được yêu cầu:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name (ví dụ: `us-east-1`, `ap-southeast-1`)
- Default output format (để trống hoặc nhập `json`)

### Cách 2: Cấu hình Thủ Công

Tạo file `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Tạo file `~/.aws/config`:

```ini
[default]
region = ap-southeast-1
```

## Bước 3: Khởi Tạo DVC trong Project

```bash
# Di chuyển vào thư mục project
cd /path/to/your/project

# Khởi tạo DVC
dvc init
```

## Bước 4: Tạo S3 Bucket

### Sử dụng AWS Console:

1. Đăng nhập vào AWS Console
2. Tìm kiếm "S3" và mở dịch vụ S3
3. Click "Create bucket"
4. Đặt tên bucket (ví dụ: `my-dvc-storage`)
5. Chọn region phù hợp
6. Click "Create bucket"

### Sử dụng AWS CLI:

```bash
aws s3 mb s3://my-dvc-storage --region ap-southeast-1
```

## Bước 5: Cấu Hình DVC Remote

```bash
# Thêm remote storage
dvc remote add -d myremote s3://my-dvc-storage/dvc-store

# Kiểm tra cấu hình
dvc remote list
```

### Cấu Hình Nâng Cao (Tùy Chọn)

```bash
# Chỉ định region cụ thể
dvc remote modify myremote region ap-southeast-1

# Sử dụng profile AWS cụ thể
dvc remote modify myremote profile myprofile

# Cấu hình credentials trực tiếp (không khuyến nghị cho production)
dvc remote modify myremote access_key_id YOUR_ACCESS_KEY
dvc remote modify myremote secret_access_key YOUR_SECRET_KEY
```

## Bước 6: Sử Dụng DVC

### Thêm Dữ Liệu vào DVC

```bash
# Thêm file hoặc thư mục dữ liệu
dvc add data/dataset.csv

# Commit file .dvc vào Git
git add data/dataset.csv.dvc data/.gitignore
git commit -m "Add dataset to DVC"
```

### Đẩy Dữ Liệu lên S3

```bash
# Push dữ liệu lên remote storage
dvc push
```

### Kéo Dữ Liệu từ S3

```bash
# Pull dữ liệu từ remote storage
dvc pull
```

### Kiểm Tra Trạng Thái

```bash
# Kiểm tra trạng thái DVC
dvc status

# Kiểm tra remote storage
dvc status --cloud
```

## Ví Dụ Workflow Hoàn Chỉnh

```bash
# 1. Khởi tạo project
git init
dvc init

# 2. Cấu hình remote
dvc remote add -d myremote s3://my-dvc-storage/project-data

# 3. Thêm dữ liệu
dvc add data/train.csv
dvc add models/model.pkl

# 4. Commit vào Git
git add data/train.csv.dvc models/model.pkl.dvc .gitignore
git commit -m "Track data and model with DVC"

# 5. Push lên S3
dvc push

# 6. Push Git repository
git push origin main
```

## Cập Nhật Data Version

### Khi Dữ Liệu Thay Đổi

Khi bạn cập nhật/thay đổi dữ liệu, DVC sẽ tự động phát hiện và tạo phiên bản mới:

```bash
# Bước 1: Thay đổi dữ liệu (ví dụ: thêm/sửa file trong thư mục data)
# ... thực hiện thay đổi dữ liệu ...

# Bước 2: Cập nhật DVC tracking
dvc add data/dataset.csv

# Bước 3: Commit file .dvc mới vào Git
git add data/dataset.csv.dvc
git commit -m "Update dataset - added 1000 new samples"

# Bước 4: Push dữ liệu mới lên S3
dvc push

# Bước 5: Push Git commit
git push origin main
```

### Workflow Cập Nhật Hoàn Chỉnh

```bash
# 1. Kiểm tra trạng thái hiện tại
dvc status

# 2. Thay đổi dữ liệu
# Ví dụ: Thêm file mới vào thư mục data/
cp new_data.csv data/

# 3. Cập nhật DVC tracking
dvc add data/

# 4. Xem thay đổi
git diff data/.dvc

# 5. Commit vào Git với message mô tả rõ ràng
git add data/.dvc
git commit -m "feat: add new_data.csv with 5000 samples"

# 6. Push lên remote storage
dvc push

# 7. Push lên Git
git push
```

### Quay Lại Phiên Bản Cũ

DVC cho phép bạn quay lại bất kỳ phiên bản dữ liệu nào thông qua Git:

```bash
# Xem lịch sử thay đổi
git log data/dataset.csv.dvc

# Checkout về commit cũ
git checkout <commit-hash> data/dataset.csv.dvc

# Pull dữ liệu của phiên bản đó
dvc checkout
```

### Ví Dụ Thực Tế

**Scenario: Cập nhật model sau khi training**

```bash
# 1. Training xong, có model mới
# models/model_v2.pkl được tạo ra

# 2. Add model mới vào DVC
dvc add models/model_v2.pkl

# 3. Commit
git add models/model_v2.pkl.dvc
git commit -m "train: update model v2 - accuracy 95%"

# 4. Push
dvc push
git push
```

**Scenario: Cập nhật toàn bộ dataset**

```bash
# 1. Thay thế dữ liệu cũ bằng dữ liệu mới
rm -rf data/train/*
cp -r /path/to/new/data/* data/train/

# 2. DVC sẽ phát hiện thay đổi
dvc status
# Output: data/train.dvc: modified

# 3. Cập nhật tracking
dvc add data/train

# 4. Commit với message chi tiết
git add data/train.dvc
git commit -m "data: update training set - 10k -> 50k samples"

# 5. Push
dvc push
git push
```

### So Sánh Phiên Bản

```bash
# Xem sự khác biệt giữa 2 commits
git diff HEAD~1 HEAD data/dataset.csv.dvc

# Xem metadata của phiên bản hiện tại
cat data/dataset.csv.dvc
```

### Best Practices cho Versioning

1. **Commit Messages Rõ Ràng**: Mô tả chi tiết thay đổi gì, tại sao

   ```bash
   git commit -m "data: add validation set (2000 samples) for model evaluation"
   ```

2. **Tag Các Phiên Bản Quan Trọng**:

   ```bash
   git tag -a v1.0-data -m "Dataset version 1.0 - baseline"
   git push origin v1.0-data
   ```

3. **Sử Dụng Branches**: Thử nghiệm với dữ liệu mới trên branch riêng

   ```bash
   git checkout -b experiment/new-augmentation
   # ... thay đổi dữ liệu ...
   dvc add data/
   git add data/.dvc
   git commit -m "experiment: test data augmentation"
   dvc push
   ```

4. **Kiểm Tra Trước Khi Push**:

   ```bash
   # Kiểm tra những gì sẽ được push
   dvc status --cloud

   # Kiểm tra kích thước
   du -sh .dvc/cache
   ```

## Làm Việc Nhóm

### Clone Repository và Pull Data

Khi đồng nghiệp clone repository:

```bash
# Clone Git repository
git clone <repository-url>
cd <repository-name>

# Pull dữ liệu từ S3
dvc pull
```

### Đồng Bộ Cập Nhật Mới

Khi có người khác cập nhật dữ liệu:

```bash
# Pull code mới từ Git
git pull

# Pull dữ liệu mới từ S3
dvc pull
```

### Xử Lý Conflicts

Nếu nhiều người cùng sửa dữ liệu:

```bash
# Fetch thay đổi mới
git fetch origin

# Merge hoặc rebase
git merge origin/main

# Nếu có conflict trong file .dvc, resolve và:
dvc checkout
```

## Xử Lý Sự Cố

### Lỗi 403 Forbidden

Nếu gặp lỗi `ERROR: unexpected error - Forbidden: An error occurred (403)`:

**Nguyên nhân phổ biến:**

1. AWS credentials không hợp lệ hoặc bị đảo ngược
2. Không có quyền truy cập S3 bucket
3. Bucket không tồn tại hoặc sai region

**Cách khắc phục:**

```bash
# Bước 1: Kiểm tra credentials có hợp lệ không
aws sts get-caller-identity
```

Nếu thấy lỗi `InvalidClientTokenId`, credentials của bạn không đúng.

**Kiểm tra file credentials:**

```bash
cat ~/.aws/credentials
```

Đảm bảo format đúng:

- `aws_access_key_id` phải bắt đầu với `AKIA...` (20 ký tự)
- `aws_secret_access_key` là chuỗi dài khoảng 40 ký tự

> [!WARNING]
> **Lỗi thường gặp**: Đảo ngược Access Key ID và Secret Access Key!
>
> ❌ **SAI:**
>
> ```ini
> aws_access_key_id = 677276117582
> aws_secret_access_key = AKIAZ3MGNNJHB6XNJW4U
> ```
>
> ✅ **ĐÚNG:**
>
> ```ini
> aws_access_key_id = AKIAZ3MGNNJHB6XNJW4U
> aws_secret_access_key = <secret-key-dài-40-ký-tự>
> ```

**Sửa credentials:**

```bash
# Cách 1: Sử dụng aws configure
aws configure

# Cách 2: Sửa trực tiếp file
nano ~/.aws/credentials
```

### Lỗi Credentials Khác

```bash
# Kiểm tra credentials
aws sts get-caller-identity

# Kiểm tra quyền truy cập S3
aws s3 ls s3://my-dvc-storage/
```

### Kiểm Tra Quyền IAM

Đảm bảo IAM user có các quyền sau:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-dvc-storage/*",
        "arn:aws:s3:::my-dvc-storage"
      ]
    }
  ]
}
```

### Lỗi Region

```bash
# Chỉ định region rõ ràng
dvc remote modify myremote region ap-southeast-1
```

### Kiểm Tra Cấu Hình DVC

```bash
# Xem tất cả cấu hình
dvc config --list

# Xem cấu hình remote
dvc remote list -v
```

## Best Practices

1. **Bảo Mật**: Không commit AWS credentials vào Git. Sử dụng AWS IAM roles hoặc environment variables.

2. **Tổ Chức Bucket**: Sử dụng prefix/folder trong S3 để tổ chức nhiều projects:

   ```bash
   dvc remote add -d myremote s3://my-dvc-storage/project-name/
   ```

3. **Gitignore**: DVC tự động tạo `.gitignore` để loại trừ dữ liệu thực tế khỏi Git.

4. **Versioning**: Commit file `.dvc` vào Git để theo dõi phiên bản dữ liệu.

5. **Cache**: DVC cache dữ liệu local tại `.dvc/cache` để tối ưu hiệu suất.

## Tài Liệu Tham Khảo

- [DVC Documentation](https://dvc.org/doc)
- [DVC with S3](https://dvc.org/doc/user-guide/data-management/remote-storage/amazon-s3)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)

## Lưu Ý Quan Trọng

- **Chi phí**: AWS S3 tính phí theo dung lượng lưu trữ và số lượng requests. Theo dõi usage để tránh chi phí bất ngờ.
- **Quyền truy cập**: Đảm bảo bucket có cấu hình quyền phù hợp (private/public).
- **Backup**: S3 có tính năng versioning riêng, có thể bật để backup thêm.
