from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên nhóm")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    def __str__(self):
        return self.name
class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Sẵn sàng'),
        ('borrowed', 'Đang cho mượn'),
        ('maintenance', 'Đang bảo trì'),
        ('broken', 'Hỏng hóc'),
    ]
    name = models.CharField(max_length=200, verbose_name="Tên thiết bị")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Nhóm thiết bị")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Mã/Serial")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Tình trạng")
    purchase_date = models.DateField(verbose_name="Ngày mua")
    description = models.TextField(blank=True, verbose_name="Ghi chú")
    def __str__(self):
        return f"{self.name} ({self.serial_number})"
class BorrowRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Thiết bị")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người mượn")
    borrow_date = models.DateTimeField(default=timezone.now, verbose_name="Ngày mượn")
    expected_return_date = models.DateTimeField(verbose_name="Ngày hẹn trả")
    actual_return_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày trả thực tế")
    is_returned = models.BooleanField(default=False, verbose_name="Đã trả")
    def __str__(self):
        return f"{self.borrower.username} mượn {self.equipment.name}"
class MaintenanceRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Thiết bị")
    maintenance_date = models.DateField(verbose_name="Ngày bảo trì")
    description = models.TextField(verbose_name="Chi tiết bảo trì")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Chi phí")
    next_maintenance_date = models.DateField(null=True, blank=True, verbose_name="Lịch bảo trì tiếp theo")

    def __str__(self):
        return f"Bảo trì {self.equipment.name} ngày {self.maintenance_date}"