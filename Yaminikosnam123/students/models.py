from django.db import models
from django.utils import timezone
from django.conf import settings


class Student(models.Model):
    GRADUATION_CHOICES = [
        ('Degree', 'Degree'),
        ('PG', 'PG'),
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

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='students'
    )
    academic_year = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    graduation = models.CharField(max_length=20, choices=GRADUATION_CHOICES, null=True, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='enrolled')

    def _str_(self):
        return f"{self.name} ({self.roll_number})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])
    module = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    total = models.FloatField(default=70.0)
    date = models.DateField()
    module = models.CharField(max_length=50, blank=True)

    @property
    def is_pass(self):
        return self.score >= 25

    def _str_(self):
        status = "Pass" if self.is_pass else "Fail"
        return f"{self.subject}: {self.score}/{self.total} ({status})"