from django.shortcuts import render
from .models import Equipment, Category

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