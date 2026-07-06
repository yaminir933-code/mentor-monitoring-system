from django.db import models
from meeting.models import Student

class CareerProfile(models.Model):
    CAREER_PATH = [
        ('higher_studies', 'Higher Studies'),
        ('job_placement', 'Job Placement'),
        ('undecided', 'Undecided'),
    ]
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    career_path = models.CharField(max_length=50, choices=CAREER_PATH, default='undecided')
    mobile_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.career_path}"

class HigherStudiesRecord(models.Model):
    GOAL_TYPES = [
        ('MSc', 'MSc'),
        ('MTech', 'MTech'),
        ('MBA', 'MBA'),
        ('PhD', 'PhD'),
        ('UPSC', 'UPSC - Civil Services'),
        ('GATE', 'GATE'),
        ('GRE', 'GRE - Abroad Studies'),
        ('Other_Exam', 'Other Competitive Exam'),
    ]
    PROGRESS_STATUS = [
        ('Not Started', 'Not Started'),
        ('Preparing', 'Preparing'),
        ('Applied', 'Applied'),
        ('Exam Cleared', 'Exam Cleared'),
        ('Admission Received', 'Admission Received'),
        ('Enrolled', 'Enrolled'),
    ]
    profile = models.ForeignKey(CareerProfile, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    interest_area = models.CharField(max_length=200)
    target_institution = models.CharField(max_length=200, blank=True)
    preparation_level = models.IntegerField(default=0)
    progress_status = models.CharField(max_length=50, choices=PROGRESS_STATUS, default='Not Started')
    exam_score = models.CharField(max_length=50, blank=True)
    guidance_plan = models.TextField(blank=True)
    resources_provided = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.student.name} - {self.goal_type}"

class PlacementRecord(models.Model):
    PLACEMENT_STATUS = [
        ('Searching', 'Searching'),
        ('Applied', 'Applied'),
        ('Interview Stage', 'Interview Stage'),
        ('Offer Received', 'Offer Received'),
        ('Placed', 'Placed'),
        ('Still Looking', 'Still Looking'),
    ]
    profile = models.ForeignKey(CareerProfile, on_delete=models.CASCADE)
    placement_office_visits = models.IntegerField(default=0)
    interviews_attended = models.IntegerField(default=0)
    interviews_cleared = models.IntegerField(default=0)
    placement_status = models.CharField(max_length=50, choices=PLACEMENT_STATUS, default='Searching')
    company_name = models.CharField(max_length=200, blank=True)
    job_role = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    job_location = models.CharField(max_length=200, blank=True)
    offer_date = models.DateField(null=True, blank=True)
    guidance_notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.student.name} - {self.placement_status}"
