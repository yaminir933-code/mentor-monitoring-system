from django.urls import path
from . import views

urlpatterns = [
    path('', views.academic_home, name='academic_home'),
    path('semester/<int:student_id>/<int:sem_number>/', views.semester_view, name='semester_view'),
    path('add-subject/<int:student_id>/<int:sem_number>/', views.add_subject, name='add_subject'),
    path('get-subjects/<int:student_id>/<int:sem_number>/', views.get_subjects_by_semester, name='get_subjects'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('add-marks/<int:student_id>/<int:sem_number>/', views.add_marks, name='add_marks'),
    path('add-attendance/<int:student_id>/<int:sem_number>/', views.add_attendance, name='add_attendance'),
    path('edit/<int:record_id>/', views.edit_academic, name='edit_academic'),
    path('delete/<int:record_id>/', views.delete_academic, name='delete_academic'),
    path('add-project/<int:student_id>/<int:sem_number>/', views.add_project, name='add_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('view/<int:student_id>/', views.view_academic, name='view_academic'),
]