from django.db import models
from meeting.models import Student
from cloudinary_storage.storage import RawMediaCloudinaryStorage
import cloudinary

class ActivityRecord(models.Model):
    ACTIVITY_TYPES = [
        ('Sports', 'Sports'),
        ('Cultural', 'Cultural Events'),
        ('Technical', 'Technical Events'),
        ('Seminar', 'Seminars'),
        ('Hackathon', 'Hackathons'),
        ('NCC', 'NCC'),
        ('NSS', 'NSS'),
        ('Arts', 'Arts & Crafts'),
        ('Literary', 'Literary Events'),
        ('Competition', 'Competitions'),
        ('Workshop', 'Workshops'),
        ('Social', 'Social Service'),
        ('College', 'College Activities'),
        ('Other', 'Other'),
    ]

    PARTICIPATION_STATUS = [
        ('Active', 'Active'),
        ('Not Participating', 'Not Participating'),
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    activity_name = models.CharField(max_length=200)
    date = models.DateField()
    participation_status = models.CharField(max_length=50, choices=PARTICIPATION_STATUS)
    achievement = models.CharField(max_length=200, blank=True)
    score = models.CharField(max_length=50, blank=True)
    reason_not_participating = models.TextField(blank=True)
    skills_gained = models.TextField(blank=True)
    guidance_notes = models.TextField(blank=True)
    encouragement_plan = models.TextField(blank=True)
    upload_file = models.FileField(
        upload_to='activity_uploads/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage(),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_upload_url(self):
        """
        Build a guaranteed https:// Cloudinary raw URL for the uploaded file.
        activity files are always uploaded via RawMediaCloudinaryStorage
        so the resource_type is always 'raw'.
        """
        if not self.upload_file or not self.upload_file.name:
            return None
        try:
            name = self.upload_file.name.strip('/')
            # If the name is already a full URL, fix the scheme and return it
            if 'cloudinary.com' in name:
                if name.startswith('https://'):
                    return name
                if name.startswith('http://'):
                    return name.replace('http://', 'https://', 1)
                if name.startswith('//'):
                    return f'https:{name}'
                return f'https://{name}'
            # Build the correct Cloudinary raw URL manually
            cloud_name = cloudinary.config().cloud_name
            if not cloud_name:
                return None
            return f"https://res.cloudinary.com/{cloud_name}/raw/upload/{name}"
        except Exception:
            return None

    def __str__(self):
        return f"{self.student.name} - {self.activity_name}"