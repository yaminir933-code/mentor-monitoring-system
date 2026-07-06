# Centralized departments configuration
# Edit this file to add, remove, or modify departments across the entire project

DEPARTMENTS = [
    'MSC Computer Science',
    'MSC Data Science',
    'MSC Statistics',
    'MSC Chemistry',
    'BBA',
    'BSC MEC',
    'BSC MSC',
]

# For Django forms (returns list of tuples)
DEPARTMENT_CHOICES = [
    ('', 'Select your department'),
    *[(dept, dept) for dept in DEPARTMENTS]
]
