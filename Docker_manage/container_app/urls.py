from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_containers, name='list_containers'),
    path('restart/<str:container_name>/', views.restart_container, name='restart_container'),
    path('reset/<str:container_name>/', views.reset_container, name='reset_container'),
    path('<str:container_name>/', views.container_detail, name='container_detail'),
]