# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('', views.home_view, name='home'),
    path('questions/loading/', views.questions_loading_view, name='questions_loading'),
    path('questions/', views.questions_view, name='questions'),
    path('answer/loading/', views.answer_loading_view, name='answer_loading'),
    path('answer/', views.answer_view, name='answer'),


    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),


    path('favorites/', views.favorites_list_view, name='favorites_list'),
    path('favorites/add/', views.add_to_favorites_view, name='add_to_favorites'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorites_view, name='remove_from_favorites'),
]