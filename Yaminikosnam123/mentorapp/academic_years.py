# Centralized academic years configuration
# Edit this file to add, remove, or modify academic years across the entire project

from datetime import datetime

def get_academic_years():
    """
    Dynamically generates academic years from current year to next 10 years.
    Returns a list of academic year strings like ['2025-26', '2026-27', ...]
    """
    current_year = datetime.now().year
    years = []
    
    # Generate years from current year backwards for 5 years and forward for 5 years
    for i in range(-2, 10):  # -5 to +5 gives 10 years range
        year = current_year + i
        next_year = year + 1
        academic_year = f"{year}-{str(next_year)[-2:]}"
        years.append(academic_year)
    
    return years

ACADEMIC_YEARS = get_academic_years()

# For Django forms (returns list of tuples)
ACADEMIC_YEAR_CHOICES = [
    ('', 'Select academic year'),
    *[(year, year) for year in ACADEMIC_YEARS]
]
