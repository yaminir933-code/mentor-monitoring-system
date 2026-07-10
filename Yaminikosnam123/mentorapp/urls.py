from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('accounts.urls')),
    path('meeting/', include('meeting.urls')),
    path('students/', include('students.urls')),
    path('academic/', include('academic.urls')),
    path('activity/', include('activity.urls')),
    path('career/', include('career_guidance.urls')),
]

# Serve media files locally only in development (DEBUG=True)
# In production, files are served from Cloudinary
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)