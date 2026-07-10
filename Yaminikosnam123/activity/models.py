from django.db import models
from meeting.models import Student
from cloudinary_storage.storage import RawMediaCloudinaryStorage
import cloudinary


def _build_cloudinary_url(file_name, cloud_name, resource_type='raw'):
    """
    Safely extract the Cloudinary public_id from whatever format is stored
    in file.name, then return a guaranteed correct https:// URL.

    Handles all of these stored formats:
      - 'activity_uploads/Screenshot_abc.png'          (clean path)
      - 'https://res.cloudinary.com/X/raw/upload/...'  (full URL)
      - 'https/res.cloudinary.com/X/...'               (broken, no colon)
      - 'res.cloudinary.com/X/...'                     (partial, no scheme)
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
        Return a guaranteed https:// Cloudinary raw URL for the activity file.
        Activity files are always stored as resource_type='raw'.
        """
        if not self.upload_file or not self.upload_file.name:
            return None
        try:
            cloud_name = cloudinary.config().cloud_name or 'wltyf291'
            return _build_cloudinary_url(self.upload_file.name, cloud_name, resource_type='raw')
        except Exception:
            return None

    def __str__(self):
        return f"{self.student.name} - {self.activity_name}"