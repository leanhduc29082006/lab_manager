from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('borrow/', views.borrow_equipment, name='borrow_equipment'),
    path('history/', views.borrow_history, name='borrow_history'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:equipment_id>/', views.equipment_maintenance, name='equipment_maintenance'),
    path('login/', auth_views.LoginView.as_view(template_name='equipment/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='equipment_list'), name='logout'),
]