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


class PersonalityDevelopment(models.Model):

    GOAL_CATEGORY = [
        ('higher_studies', 'Preparing for Higher Studies'),
        ('job_placement',  'Preparing for Job Placement'),
        ('both',           'Both Higher Studies & Job'),
        ('general',        'General Development'),
    ]

    SOFT_SKILL_LEVELS = [
        ('none',     'Not Developed'),
        ('beginner', 'Beginner'),
        ('average',  'Average'),
        ('good',     'Good'),
        ('excellent','Excellent'),
    ]

    PERSONAL_ISSUE_CHOICES = [
        ('none',        'None'),
        ('confidence',  'Lack of Confidence'),
        ('anxiety',     'Exam / Interview Anxiety'),
        ('family',      'Family Pressure / Issues'),
        ('financial',   'Financial Difficulties'),
        ('health',      'Health Issues'),
        ('peer',        'Peer Pressure'),
        ('motivation',  'Lack of Motivation'),
        ('time_mgmt',   'Poor Time Management'),
        ('other',       'Other'),
    ]

    STATUS_CHOICES = [
        ('identified',   'Identified'),
        ('in_progress',  'In Progress'),
        ('improved',     'Improved'),
        ('resolved',     'Resolved'),
    ]

    profile      = models.ForeignKey(CareerProfile, on_delete=models.CASCADE)
    goal_category = models.CharField(max_length=30, choices=GOAL_CATEGORY, default='general')
    recorded_date = models.DateField()

    # ── Skills gap ────────────────────────────────────────────
    technical_skills_gap   = models.TextField(blank=True,
        help_text='List technical skills the student is missing (e.g. Python, SQL, Excel)')
    soft_skills_gap        = models.TextField(blank=True,
        help_text='Communication, leadership, teamwork gaps etc.')
    communication_level    = models.CharField(max_length=20, choices=SOFT_SKILL_LEVELS, default='average')
    leadership_level       = models.CharField(max_length=20, choices=SOFT_SKILL_LEVELS, default='average')
    problem_solving_level  = models.CharField(max_length=20, choices=SOFT_SKILL_LEVELS, default='average')

    # ── Personal challenges ────────────────────────────────────
    personal_issue         = models.CharField(max_length=30, choices=PERSONAL_ISSUE_CHOICES, default='none')
    personal_issue_details = models.TextField(blank=True,
        help_text='Describe the personal challenge in detail')
    emotional_state        = models.TextField(blank=True,
        help_text="Student's current emotional / mental well-being notes")

    # ── Mentor action plan ─────────────────────────────────────
    mentor_observations    = models.TextField(blank=True,
        help_text='What the mentor observed about the student')
    action_plan            = models.TextField(blank=True,
        help_text='Steps planned to help the student')
    resources_suggested    = models.TextField(blank=True,
        help_text='Books, courses, workshops, counselling suggested')
    follow_up_date         = models.DateField(null=True, blank=True)

    # ── Progress ───────────────────────────────────────────────
    status                 = models.CharField(max_length=20, choices=STATUS_CHOICES, default='identified')
    progress_notes         = models.TextField(blank=True,
        help_text='Progress noted at follow-up')

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile.student.name} – Personality Dev ({self.recorded_date})"
