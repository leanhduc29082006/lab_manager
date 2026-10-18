# Lab Manager
Hệ thống quản lý thiết bị phòng Lab được xây dựng bằng **Django**.
## Quick start
### 1. Installation
Clone project và cài đặt Django:
```bash
git clone <repository-url>
cd web
python -m venv venv
venv\Scripts\activate
pip install django==6.1.2
```
### 2. Database
Khởi tạo database:
```bash
python manage.py makemigrations
python manage.py migrate
```
Tạo tài khoản quản trị:
```bash
python manage.py createsuperuser
```
### 3. Run project
Khởi động server:
```bash
python manage.py runserver
```
Truy cập:
```text
http://127.0.0.1:8000/
```
Trang quản trị:
```text
http://127.0.0.1:8000/admin/
```
### 4. Main features
- Quản lý thiết bị và danh mục thiết bị.
- Tìm kiếm và lọc thiết bị.
- Đăng ký mượn và trả thiết bị.
- Xem lịch sử mượn.
- Quản lý lịch sử bảo trì.
- Dashboard thống kê thiết bị.
- Đăng nhập và phân quyền người dùng.
### 5. Run tests
```bash
python manage.py test
```
### Technologies
- Python
- Django 6.1.2
- SQLite
- HTML/CSS
- Bootstrap 5.3.3
