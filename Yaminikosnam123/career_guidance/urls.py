from django.urls import path
from . import views

urlpatterns = [
    path('', views.career_home),
    path('profile/<int:student_id>', views.career_profile),
    path('set-path/<int:student_id>', views.set_career_path),
    path('add-higher/<int:student_id>', views.add_higher_studies),
    path('add-placement/<int:student_id>', views.add_placement),
    path('add-personality/<int:student_id>', views.add_personality),
    path('edit-personality/<int:record_id>', views.edit_personality),
    path('delete-personality/<int:record_id>', views.delete_personality),
    path('report', views.career_report),
    path('delete-higher/<int:record_id>', views.delete_higher),
    path('delete-placement/<int:record_id>', views.delete_placement),
    path('edit-higher/<int:record_id>', views.edit_higher),
    path('edit-placement/<int:record_id>', views.edit_placement),
    path('delete-profile/<int:student_id>', views.delete_career_profile),
]