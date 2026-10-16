from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BorrowForm, MaintenanceRecordForm
from .models import BorrowRecord, Category, Equipment, MaintenanceRecord


def equipment_list(request):
    equipments = Equipment.objects.select_related('category').all().order_by('name')
    categories = Category.objects.all()

    search_query = request.GET.get('q', '').strip()
    if search_query:
        equipments = equipments.filter(
            Q(name__icontains=search_query)
            | Q(serial_number__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    category_id = request.GET.get('category')
    if category_id:
        equipments = equipments.filter(category_id=category_id)

    status_filter = request.GET.get('status')
    if status_filter:
        equipments = equipments.filter(status=status_filter)

    context = {
        'equipments': equipments,
        'categories': categories,
        'selected_category': category_id,
        'selected_status': status_filter,
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
        records = BorrowRecord.objects.select_related('equipment', 'borrower').all().order_by('-borrow_date')
    else:
        records = BorrowRecord.objects.select_related('equipment', 'borrower').filter(borrower=request.user).order_by('-borrow_date')

    return render(request, 'equipment/borrow_history.html', {'records': records, 'now': timezone.now()})


@login_required
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def dashboard(request):
    available_count = Equipment.objects.filter(status='available').count()
    broken_count = Equipment.objects.filter(status='broken').count()
    overdue_records = BorrowRecord.objects.filter(
        is_returned=False,
        expected_return_date__lt=timezone.now(),
    ).select_related('equipment', 'borrower').order_by('-expected_return_date')

    context = {
        'available_count': available_count,
        'broken_count': broken_count,
        'overdue_records': overdue_records,
        'overdue_count': overdue_records.count(),
    }
    return render(request, 'equipment/dashboard.html', context)


@login_required
def maintenance_list(request):
    records = MaintenanceRecord.objects.select_related('equipment').order_by('-maintenance_date')
    return render(
        request,
        'equipment/maintenance_history.html',
        {'records': records, 'equipment': None, 'show_form': False, 'form': None},
    )


@login_required
def equipment_maintenance(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    records = MaintenanceRecord.objects.filter(equipment=equipment).order_by('-maintenance_date')

    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance_record = form.save(commit=False)
            maintenance_record.equipment = equipment
            maintenance_record.save()
            equipment.status = 'maintenance'
            equipment.save()
            messages.success(request, f"Đã lưu lịch sử bảo trì cho {equipment.name}.")
            return redirect('equipment_maintenance', equipment_id=equipment.id)
    else:
        form = MaintenanceRecordForm()

    context = {
        'equipment': equipment,
        'records': records,
        'form': form,
        'show_form': True,
    }
    return render(request, 'equipment/maintenance_history.html', context)