from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/add/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/toggle/', views.toggle_complete, name='toggle_complete'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_page, name='registration'),
]