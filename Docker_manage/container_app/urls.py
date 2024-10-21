from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_containers, name='list_containers'),
    path('<str:container_name>/manage/restart', views.restart_container, name='restart_container'),
    path('<str:container_name>/manage/reset', views.reset_container, name='reset_container'),
    path('<str:container_name>/manage', views.container_detail, name='container_detail'),
]