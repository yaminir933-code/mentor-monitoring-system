from django.contrib import admin
from .models import AcademicRecord, Subject, Project, SubjectCatalog

@admin.register(SubjectCatalog)
class SubjectCatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course_type', 'semester')
    list_filter = ('course_type', 'semester')
    search_fields = ('name', 'code')
    ordering = ('course_type', 'semester', 'name')

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'subject', 'total_marks', 'result')
    list_filter = ('semester', 'result')
    search_fields = ('student__name', 'subject')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'name')
    list_filter = ('semester',)
    search_fields = ('student__name', 'name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'name', 'created_at')
    list_filter = ('semester',)
    search_fields = ('student__name', 'name')
