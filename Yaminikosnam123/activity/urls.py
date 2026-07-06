from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_home),
    path('add/<int:student_id>/', views.add_activity),
    path('view/<int:student_id>/', views.view_activity),
    path('edit/<int:record_id>/', views.edit_activity),
    path('delete/<int:record_id>/', views.delete_activity),
]