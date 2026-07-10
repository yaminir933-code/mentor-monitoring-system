from django.db import models
from meeting.models import Student
from cloudinary_storage.storage import RawMediaCloudinaryStorage
import cloudinary

class SubjectCatalog(models.Model):
    """Predefined subjects for degree and PG programs"""
    COURSE_CHOICES = [
        ('Degree', 'Degree'),
        ('PG', 'Post Graduation (PG)'),
    ]
    course_type = models.CharField(max_length=10, choices=COURSE_CHOICES)
    semester = models.IntegerField()  # 1-6 for Degree, 1-4 for PG
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)  # Optional subject code

    class Meta:
        unique_together = ('course_type', 'semester', 'name')

    def __str__(self):
        return f"{self.course_type} - Sem {self.semester} - {self.name}"

class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    subject = models.CharField(max_length=200)
    internal_marks = models.FloatField(default=0)
    external_marks = models.FloatField(default=0)
    assignments = models.FloatField(default=0)  # NEW: Assignments marks
    total_marks = models.FloatField(default=0)
    result = models.CharField(max_length=10, default='Fail')
    total_classes = models.IntegerField(default=0)
    attended_classes = models.IntegerField(default=0)
    attendance_percentage = models.FloatField(default=0)
    guidance_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Sem {self.semester} - {self.subject}"

class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    name = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='projects/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage(),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        """Return the correct Cloudinary URL for the project file."""
        if not self.file:
            return None
        try:
            url, _ = cloudinary.utils.cloudinary_url(
                self.file.name,
                resource_type='raw',
                secure=True,
            )
            return url
        except Exception:
            return None

    def __str__(self):
        return self.name