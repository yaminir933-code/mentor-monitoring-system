from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_home),
    path('add/<int:student_id>', views.add_meeting),
    path('bulk-add/', views.bulk_add_meeting, name='bulk_add_meeting'),
    path('view/<int:student_id>', views.view_meetings),
    path('edit/<int:meeting_id>', views.edit_meeting),
    path('delete/<int:meeting_id>', views.delete_meeting),
]