# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Наши кастомные страницы
    path('', views.home_view, name='home'),
    path('questions/', views.questions_view, name='questions'),
    path('answer/', views.answer_view, name='answer'),

    # Страницы аутентификации
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]