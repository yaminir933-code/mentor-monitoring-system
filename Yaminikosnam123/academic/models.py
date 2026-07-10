from django.db import models
from meeting.models import Student
from cloudinary_storage.storage import MediaCloudinaryStorage
import cloudinary

def _build_cloudinary_url(file_name, cloud_name, resource_type='image'):
    """
    Safely extract the Cloudinary public_id from whatever format is stored
    in file.name, then return a guaranteed correct https:// URL.
    """
    if not file_name:
        return None

    name = file_name.strip()

    # If a /upload/ separator exists, everything AFTER it is the public_id
    if '/upload/' in name:
        public_id = name.split('/upload/', 1)[1]
    elif 'res.cloudinary.com' in name:
        # No /upload/ found – strip everything up to and including the cloud_name
        marker = f'/{cloud_name}/'
        if marker in name:
            remainder = name.split(marker, 1)[1]
            # Strip resource-type prefix if present  e.g. 'image/', 'raw/'
            for rt in ('image/', 'raw/', 'video/'):
                if remainder.startswith(rt):
                    remainder = remainder[len(rt):]
                    break
            public_id = remainder
        else:
            public_id = name
    else:
        # Plain path – use as-is
        public_id = name

    public_id = public_id.strip('/')
    if not public_id:
        return None

    return f"https://res.cloudinary.com/{cloud_name}/{resource_type}/upload/{public_id}"

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
            cloud_name = cloudinary.config().cloud_name or 'wltyf291'
            return _build_cloudinary_url(self.file.name, cloud_name, resource_type='image')
        except Exception:
            return None

    def __str__(self):
        return self.name