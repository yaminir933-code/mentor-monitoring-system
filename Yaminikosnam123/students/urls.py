from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_home),
    path('delete/<int:student_id>/', views.delete_student),
    path('pdf/<int:student_id>/', views.generate_pdf, name='generate_pdf'),
    path('pipeline/', views.pipeline_view, name='pipeline'),
    path('update-stage/<int:student_id>/', views.update_stage, name='update_stage'),
]