from django.core.management.base import BaseCommand
from academic.models import SubjectCatalog

class Command(BaseCommand):
    help = 'Populate SubjectCatalog with default subjects for Degree and PG programs'

    def handle(self, *args, **options):
        # Degree subjects (6 semesters)
        degree_subjects = {
            1: [
                'Mathematics I', 'Physics I', 'Chemistry I', 'Programming Fundamentals', 
                'Engineering Graphics', 'Environmental Science'
            ],
            2: [
                'Mathematics II', 'Physics II', 'Chemistry II', 'Data Structures',
                'Digital Logic Design', 'Communication Skills'
            ],
            3: [
                'Discrete Mathematics', 'Algorithms', 'Object-Oriented Programming',
                'Database Systems', 'Web Technologies', 'Operating Systems'
            ],
            4: [
                'Software Engineering', 'Computer Networks', 'Database Management',
                'System Design', 'Advanced Web Development', 'Mobile Applications'
            ],
            5: [
                'Machine Learning', 'Cloud Computing', 'Cybersecurity',
                'Big Data Analytics', 'Artificial Intelligence', 'DevOps'
            ],
            6: [
                'Project Management', 'Entrepreneurship', 'Professional Ethics',
                'Technical Writing', 'Advanced Topics', 'Capstone Project'
            ]
        }

        # PG subjects (4 semesters)
        pg_subjects = {
            1: [
                'Advanced Algorithms', 'Machine Learning', 'Natural Language Processing',
                'Research Methodology', 'Advanced Database Systems'
            ],
            2: [
                'Deep Learning', 'Computer Vision', 'Distributed Systems',
                'Advanced Network Security', 'Cloud Architecture'
            ],
            3: [
                'Advanced Machine Learning', 'Reinforcement Learning', 'Neural Networks',
                'Big Data Analytics', 'Advanced Optimization'
            ],
            4: [
                'Project Dissertation', 'Research Colloquium', 'Advanced Topics Seminar',
                'Industry Internship', 'Thesis Work'
            ]
        }

        created_count = 0

        # Create Degree subjects
        for semester, subjects in degree_subjects.items():
            for subject_name in subjects:
                obj, created = SubjectCatalog.objects.get_or_create(
                    course_type='Degree',
                    semester=semester,
                    name=subject_name
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created: Degree - Sem {semester} - {subject_name}'
                    ))

        # Create PG subjects
        for semester, subjects in pg_subjects.items():
            for subject_name in subjects:
                obj, created = SubjectCatalog.objects.get_or_create(
                    course_type='PG',
                    semester=semester,
                    name=subject_name
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created: PG - Sem {semester} - {subject_name}'
                    ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Successfully created {created_count} subjects!'
        ))
