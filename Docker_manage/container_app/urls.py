from django.urls import path
from . import views

urlpatterns = [
    # 展示所有容器
    path('', views.list_containers, name='list_containers'),

    # 常规容器管理
    path('<str:container_name>/manage/restart', views.restart_container, name='restart_container'),
    path('<str:container_name>/manage/reset', views.reset_container, name='reset_container'),
    path('<str:container_name>/manage', views.container_detail, name='container_detail'),

    # 学生 MySQL 容器管理
    path('<str:container_name>/manage/reset/mysql', views.reset_mysql_container, name='reset_mysql_container'),
    path('<str:container_name>/manage/restart/mysql', views.restart_mysql_container, name='restart_mysql_container'),
]