from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_edit_view, name='profile_edit'),
    
    # Success Analytics
    path('success-analytics/', views.success_analytics, name='success_analytics'),
    
    # Analytics (if needed)
    path('analytics/', views.analytics_view, name='analytics'),
    
    # TODO: Add these views later
    # path('add-student/', views.add_student, name='add_student'),
    # path('manage-students/', views.manage_students, name='manage_students'),
]