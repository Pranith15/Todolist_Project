from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('task/new/', views.task_create_view, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update_view, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete_view, name='task_delete'),
    path('task/<int:pk>/toggle/', views.task_toggle_complete_view, name='task_toggle'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
