from django.contrib import admin
from .models import Category, Equipment, BorrowRecord, MaintenanceRecord
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'status')
    list_filter = ('status', 'category')
    search_fields = ('name', 'serial_number')
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'borrower', 'borrow_date', 'is_returned')
    list_filter = ('is_returned', 'borrow_date')
admin.site.register(Category)
admin.site.register(MaintenanceRecord)