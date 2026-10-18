from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('routes/', views.route_list, name='route_list'),
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),
    path('excursion/<int:excursion_id>/join/', views.join_excursion, name='join_excursion'),
    
    path('admin-panel/route/add/', views.route_create, name='route_create'),
    path('admin-panel/route/<int:pk>/edit/', views.route_update, name='route_update'),
    path('admin-panel/route/<int:pk>/delete/', views.route_delete, name='route_delete'),
    
    path('admin-panel/excursion/add/', views.excursion_create, name='excursion_create'),
    path('admin-panel/excursion/<int:pk>/edit/', views.excursion_update, name='excursion_update'),
    path('admin-panel/excursion/<int:pk>/delete/', views.excursion_delete, name='excursion_delete'),
    
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]