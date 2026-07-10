from django.db import models
from meeting.models import Student
from cloudinary_storage.storage import MediaCloudinaryStorage
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
    # Use MediaCloudinaryStorage so all files (old and new) are image/raw type.
    # Cloudinary accepts PNG/JPG/PDF under the image resource type.
    file = models.FileField(
        upload_to='projects/',
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage(),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        """
        Build a guaranteed https:// Cloudinary URL for the project file.
        Files uploaded via MediaCloudinaryStorage use resource_type='image'.
        URL format: https://res.cloudinary.com/{cloud}/image/upload/{name}
        """
        if not self.file or not self.file.name:
            return None
        try:
            name = self.file.name.strip('/')
            # If the name is already a full URL, fix the scheme and return it
            if 'cloudinary.com' in name:
                if name.startswith('https://'):
                    return name
                if name.startswith('http://'):
                    return name.replace('http://', 'https://', 1)
                if name.startswith('//'):
                    return f'https:{name}'
                return f'https://{name}'
            # Build the correct Cloudinary image URL manually
            cloud_name = cloudinary.config().cloud_name
            if not cloud_name:
                return None
            return f"https://res.cloudinary.com/{cloud_name}/image/upload/{name}"
        except Exception:
            return None

    def __str__(self):
        return self.name