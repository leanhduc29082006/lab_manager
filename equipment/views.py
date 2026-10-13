from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Equipment, Category, BorrowRecord
from .forms import BorrowForm

# Hàm hiển thị danh sách thiết bị (Hàm đang bị thiếu gây ra lỗi)
def equipment_list(request):
    equipments = Equipment.objects.all()
    categories = Category.objects.all()
    
    # Logic tìm kiếm
    search_query = request.GET.get('q')
    if search_query:
        equipments = equipments.filter(name__icontains=search_query)
        
    # Logic lọc theo nhóm
    category_id = request.GET.get('category')
    if category_id:
        equipments = equipments.filter(category_id=category_id)

    context = {
        'equipments': equipments,
        'categories': categories,
    }
    return render(request, 'equipment/equipment_list.html', context)

# Hàm xử lý form mượn thiết bị
@login_required
def borrow_equipment(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            borrow_record.borrower = request.user 
            borrow_record.save() 
            
            messages.success(request, f"Bạn đã mượn thành công thiết bị: {borrow_record.equipment.name}")
            return redirect('borrow_history')
    else:
        form = BorrowForm()
    
    return render(request, 'equipment/borrow_form.html', {'form': form})

# Hàm xem lịch sử mượn
@login_required
def borrow_history(request):
    if request.user.is_superuser or request.user.is_staff:
        # Nếu là Admin: Xem toàn bộ lịch sử
        records = BorrowRecord.objects.all().order_by('-borrow_date')
    else:
        # Nếu là User thường: Chỉ xem thiết bị mình mượn
        records = BorrowRecord.objects.filter(borrower=request.user).order_by('-borrow_date')
        
    return render(request, 'equipment/borrow_history.html', {'records': records})