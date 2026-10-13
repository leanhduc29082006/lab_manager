
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('borrow/', views.borrow_equipment, name='borrow_equipment'),
    path('history/', views.borrow_history, name='borrow_history'),
    path('login/', auth_views.LoginView.as_view(template_name='equipment/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='equipment_list'), name='logout'),
]