# Bài tập lớn dataware house về Sales

## 1.Giới thiệu
Backend hệ hỗ trợ quyết định bao gồm
- **Production database**: Tìm hiểu, chọn lọc các dữ liệu cần thiết từ file dữ liệu và xây dựng hệ cơ sở dữ liệu vận hành (production database) dựa trên đề tài sales cho hệ thống.
- **Analysis database**: Hệ cơ sở dữ liệu phân tích (analysis database) sử dụng các mô hình data warehouse.
- **Extract, Transform and Load**: Xây dựng pipeline ETL di chuyển dữ liệu vận hành sang hệ cơ sở dữ liệu phân tích.
- **Ứng dụng CRUD**: Hiện thực ứng dụng có các tính năng CRUD cho hệ thống.
- **Dashboard**: Xây dựng dashboard hiển thị thông tin. Dashboard có các biểu đồ, thông tin được trình bày rõ ràng, dễ hiểu và liên quan đến usecase của hệ thống. 
- **Phân tích**: Áp dụng các tính năng của AI như: prompt engineering, chat completion và function calling để rút ra các đánh giá hoặc dự đoán trên các thông tin hay dữ liệu hiện có.

Hệ cơ sở dữ liệu production:
![image_alt](https://github.com/Marky303/SalesAnalysis/blob/4afa7f8f28cb450aa572375f136b20a02112d69f/images/mapping.png)

Hệ cơ sở dữ liệu analysis:
![image_alt]([https://github.com/Marky303/SalesAnalysis/blob/4afa7f8f28cb450aa572375f136b20a02112d69f/images/mapping.png](https://github.com/Marky303/SalesAnalysis/blob/8e2f60afa4297202f11ce9ea43be43b3d4e464f8/images/Datawarehosue.png)


Một phần dữ liệu mẫu: 
![image_alt]([https://github.com/Marky303/SalesAnalysis/blob/4afa7f8f28cb450aa572375f136b20a02112d69f/images/mapping.png](https://github.com/Marky303/SalesAnalysis/blob/8e2f60afa4297202f11ce9ea43be43b3d4e464f8/images/example1.png)
![image_alt]([https://github.com/Marky303/SalesAnalysis/blob/4afa7f8f28cb450aa572375f136b20a02112d69f/images/mapping.png](https://github.com/Marky303/SalesAnalysis/blob/8e2f60afa4297202f11ce9ea43be43b3d4e464f8/images/example2.png)

## 3.Cách clone backend (IMPORTANT)
### Bước 1: Clone repo của backend về
- 1a. Mở CMD và CD vào folder cần clone backend

- 1b. Gõ lệnh sau để clone repo github của backend
```
git clone https://github.com/Marky303/SalesAnalysis
```

- 1c. Sau khi clone, CD vào SalesAnalysis. Folder của backend sẽ như sau
```
cd SalesAnalysis
```

### Bước 2: Tải các thư viện 
- 2a. Trước khi tải thư viện, trên máy phải có 
    + Python (Python 3.11+ thì càng tốt)
    + Pip ([link](https://packaging.python.org/en/latest/tutorials/installing-packages/))


- 2b. Install thư viện tạo môi trường ảo virtualenv 
```
pip install virtualenv
```

- 2c. Tạo môi trường ảo
```
virtualenv env
```
> [!WARNING]
> Sau khi tạo môi trường ảo trong folder của backend sẽ có thêm folder "env"

- 2d. Vào môi trường ảo
``` 
env\Scripts\activate
```
> [!WARNING]
> Sau khi vào môi trường ảo, CMD sẽ hiện "(env)" trước các lệnh

- 2e. Cài đặt các thư viện cần thiết bằng cách gõ lệnh sau
```
pip install -r requirements.txt
```
> [!WARNING]
> Cài đặt có thể mất 5-10p

### Bước 3: Chạy jupyter
- 3a. Trước khi chạy jupyter cần phải đảm bảo (nếu vừa clone xong thì bỏ qua điểm này)
    + Thứ nhất: Pull các update mới nhất từ repo
    ```
    git pull origin main
    ```
    > Lấy các cập nhật mới nhất từ repo

    + Thứ hai: Đã vào môi trường ảo (quan trọng)
    ```
    env\Scripts\activate
    ```
    > Sau khi vào môi trường ảo, CMD sẽ hiện (env) trước các lệnh

    + Cuối cùng: Đã install các library mới nhất 
    ```
    pip install -r requirements.txt
    ```
    > Cài các library mới nhất vì repo có thể thêm các thư viện mới.

- 3b. Sau khi đã đảm bảo các bước trên, chạy backend bằng cách gõ lệnh
```
python manage.py shell_plus --notebook
```


### Bước 4: Chạy backend
- 4a. Trước khi chạy backend cần phải đảm bảo (nếu vừa clone xong thì bỏ qua điểm này)
    + Thứ nhất: Pull các update mới nhất từ repo
    ```
    git pull origin main
    ```
    > Lấy các cập nhật mới nhất từ repo

    + Thứ hai: Đã vào môi trường ảo (quan trọng)
    ```
    env\Scripts\activate
    ```
    > Sau khi vào môi trường ảo, CMD sẽ hiện (env) trước các lệnh

    + Cuối cùng: Đã install các library mới nhất 
    ```
    pip install -r requirements.txt
    ```
    > Cài các library mới nhất vì repo có thể thêm các thư viện mới.

- 4b. Sau khi đã đảm bảo các bước trên, chạy backend bằng cách gõ lệnh
```
python manage.py runserver
```






