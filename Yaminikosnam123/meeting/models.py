from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GRADUATION_CHOICES = [
        ('Degree', 'Degree'),
        ('PG', 'Post Graduation (PG)'),
    ]
    STAGE_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('active', 'Active'),
        ('at_risk', 'At Risk'),
        ('supply', 'Supply/Arrear'),
        ('cleared', 'Cleared'),
        ('career_ready', 'Career Ready'),
        ('graduated', 'Graduated'),
    ]
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    graduation = models.CharField(max_length=10, choices=GRADUATION_CHOICES, default='Degree')
    academic_year = models.CharField(max_length=10, default='2025-26')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='enrolled')

    def __str__(self):
        return self.name

class Meeting(models.Model):
    MEETING_TYPES = [
        ('academic', 'Academic'),
        ('activity', 'Activity'),
        ('career', 'Career'),
        ('general', 'General'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    discussion = models.TextField()
    guidance = models.TextField()
    follow_up = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"