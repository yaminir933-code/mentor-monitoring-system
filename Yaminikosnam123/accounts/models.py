from django.db import models
from django.contrib.auth.models import User

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.username} - {self.department}"
class Student(models.Model):
    DEGREE_CHOICES = [
        ('degree', 'Degree'),
        ('pg', 'Post Graduation (PG)'),
    ]
    full_name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    student_type = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
