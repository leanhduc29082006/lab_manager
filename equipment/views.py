from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Equipment, Category, BorrowRecord
from .forms import BorrowForm
def equipment_list(request):
    equipments = Equipment.objects.all()
    categories = Category.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        equipments = equipments.filter(name__icontains=search_query)
    category_id = request.GET.get('category')
    if category_id:
        equipments = equipments.filter(category_id=category_id)
    context = {
        'equipments': equipments,
        'categories': categories,
    }
    return render(request, 'equipment/equipment_list.html', context)
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
@login_required
def borrow_history(request):
    if request.user.is_superuser or request.user.is_staff:
        records = BorrowRecord.objects.all().order_by('-borrow_date')
    else:
        records = BorrowRecord.objects.filter(borrower=request.user).order_by('-borrow_date')
    return render(request, 'equipment/borrow_history.html', {'records': records})