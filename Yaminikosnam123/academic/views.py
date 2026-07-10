from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from meeting.models import Student
from .models import AcademicRecord, Subject, Project, SubjectCatalog

@login_required(login_url='/login')
def academic_home(request):
    if request.GET.get('year'):
        selected_year = request.GET.get('year')
        request.session['selected_year'] = selected_year
    else:
        selected_year = request.session.get('selected_year', '2025-26')

    if selected_year == 'all':
        students = Student.objects.filter(mentor=request.user).order_by('department')
    else:
        students = Student.objects.filter(mentor=request.user, academic_year=selected_year).order_by('department')

    all_years = Student.objects.filter(mentor=request.user).values_list('academic_year', flat=True).distinct().order_by('academic_year')

    student_data = []
    for student in students:
        records = AcademicRecord.objects.filter(student=student)
        avg_marks = 0
        avg_attendance = 0
        total_pass = 0
        total_fail = 0
        if records:
            avg_marks = round(sum([r.total_marks for r in records]) / len(records), 1)
            avg_attendance = round(sum([r.attendance_percentage for r in records]) / len(records), 1)
            total_pass = records.filter(result='Pass').count()
            total_fail = records.filter(result='Fail').count()
        student_data.append({
            'student': student,
            'avg_marks': avg_marks,
            'avg_attendance': avg_attendance,
            'total_pass': total_pass,
            'total_fail': total_fail,
        })

    return render(request, 'academic/home.html', {
        'students': students,
        'student_data': student_data,
        'selected_year': selected_year,
        'all_years': all_years,
    })

    # Build chart data for each student
    student_data = []
    for student in students:
        records = AcademicRecord.objects.filter(student=student)
        avg_marks = 0
        avg_attendance = 0
        total_pass = 0
        total_fail = 0
        if records:
            avg_marks = round(sum([r.total_marks for r in records]) / len(records), 1)
            avg_attendance = round(sum([r.attendance_percentage for r in records]) / len(records), 1)
            total_pass = records.filter(result='Pass').count()
            total_fail = records.filter(result='Fail').count()
        student_data.append({
            'student': student,
            'avg_marks': avg_marks,
            'avg_attendance': avg_attendance,
            'total_pass': total_pass,
            'total_fail': total_fail,
        })

    return render(request, 'academic/home.html', {
        'students': students,
        'student_data': student_data,
    })

@login_required(login_url='/login')
def semester_view(request, student_id, sem_number):
    student = get_object_or_404(Student, id=student_id)
    records = AcademicRecord.objects.filter(student=student, semester=sem_number).order_by('subject')
    subjects = Subject.objects.filter(student=student, semester=sem_number)
    is_last_sem = (student.graduation == 'PG' and sem_number == 4) or (student.graduation == 'Degree' and sem_number == 6)
    project = Project.objects.filter(student=student, semester=sem_number).first()
    total_marks = sum([r.total_marks for r in records])
    total_attended = sum([r.attended_classes for r in records])
    total_classes = sum([r.total_classes for r in records])
    overall_attendance = round((total_attended / total_classes) * 100) if total_classes > 0 else 0
    return render(request, 'academic/semester.html', {
        'student': student,
        'sem_number': sem_number,
        'records': records,
        'subjects': subjects,
        'is_last_sem': is_last_sem,
        'project': project,
        'total_marks': total_marks,
        'total_attended': total_attended,
        'total_classes': total_classes,
        'overall_attendance': overall_attendance,
    })

@login_required(login_url='/login')
def add_subject(request, student_id, sem_number):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        subject_names = []

        if 'subject_names' in request.POST:
            subject_names = [n for n in request.POST.getlist('subject_names') if n]
            for name in subject_names:
                Subject.objects.get_or_create(
                    student=student,
                    semester=sem_number,
                    name=name
                )
        else:
            name = request.POST.get('subject_name')
            if name:
                subject_names = [name]
                Subject.objects.get_or_create(student=student, semester=sem_number, name=name)

        # If "apply to all students" checkbox is ticked, copy to every student of this mentor
        if request.POST.get('apply_to_all') == 'yes' and subject_names:
            all_students = Student.objects.filter(
                mentor=request.user
            ).exclude(id=student.id)
            for other_student in all_students:
                for name in subject_names:
                    Subject.objects.get_or_create(
                        student=other_student,
                        semester=sem_number,
                        name=name
                    )

    return redirect(f'/academic/semester/{student_id}/{sem_number}/')


@login_required(login_url='/login')
def apply_subjects_to_department(request, student_id, sem_number):
    """
    Copy ALL subjects currently saved for this student+semester
    to every other student under this mentor (all departments).
    Triggered by the standalone 'Apply to All Students' button.
    """
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.filter(student=student, semester=sem_number)

    if subjects.exists():
        all_students = Student.objects.filter(
            mentor=request.user,
        ).exclude(id=student.id)

        applied_to = 0
        for other_student in all_students:
            for subj in subjects:
                Subject.objects.get_or_create(
                    student=other_student,
                    semester=sem_number,
                    name=subj.name
                )
            applied_to += 1

        return redirect(
            f'/academic/semester/{student_id}/{sem_number}/'
            f'?apply_success={applied_to}'
        )

    return redirect(f'/academic/semester/{student_id}/{sem_number}/?apply_error=no_subjects')

@login_required(login_url='/login')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        name = request.POST.get('subject_name')
        if name:
            subject.name = name
            subject.save()
    return redirect(f'/academic/semester/{subject.student.id}/{subject.semester}/')

@login_required(login_url='/login')
def get_subjects_by_semester(request, student_id, sem_number):
    """API endpoint to fetch available subjects for a semester based on course type"""
    student = get_object_or_404(Student, id=student_id)
    course_type = student.graduation  # 'Degree' or 'PG'
    
    available_subjects = SubjectCatalog.objects.filter(
        course_type=course_type,
        semester=sem_number
    ).values_list('name', flat=True).order_by('name')
    
    already_added = Subject.objects.filter(
        student=student,
        semester=sem_number
    ).values_list('name', flat=True)
    
    return JsonResponse({
        'subjects': list(available_subjects),
        'already_added': list(already_added),
        'course_type': course_type
    })

@login_required(login_url='/login')
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    student_id = subject.student.id
    sem = subject.semester
    subject.delete()
    return redirect(f'/academic/semester/{student_id}/{sem}/')

@login_required(login_url='/login')
def add_marks(request, student_id, sem_number):
    student = get_object_or_404(Student, id=student_id)
    error = None
    success = None
    if request.method == 'POST':
        subject = request.POST.get('subject')
        internal = request.POST.get('internal_marks')
        external = request.POST.get('external_marks')
        assignments = request.POST.get('assignments', 0)
        guidance = request.POST.get('guidance_notes', '')
        try:
            internal_val = float(internal)
            external_val = float(external)
            assignments_val = float(assignments) if assignments else 0
            
            # Calculate total marks: Internal + External + Assignments
            total_marks = internal_val + external_val + assignments_val
            # Pass threshold: 60 marks out of 120 (50% - standard academic pass)
            result = 'Pass' if total_marks >= 60 else 'Fail'
            
            # Check if a record already exists for this subject
            record = AcademicRecord.objects.filter(
                student=student,
                semester=sem_number,
                subject=subject
            ).first()
            
            if record:
                # Update existing record (preserve attendance data if already entered)
                record.internal_marks = internal_val
                record.external_marks = external_val
                record.assignments = assignments_val
                record.total_marks = total_marks
                record.result = result
                record.guidance_notes = guidance
                record.save()
            else:
                # Create new record - do NOT set attendance to 0, leave as null/0 for user to fill
                AcademicRecord.objects.create(
                    student=student,
                    semester=sem_number,
                    subject=subject,
                    internal_marks=internal_val,
                    external_marks=external_val,
                    assignments=assignments_val,
                    total_marks=total_marks,
                    result=result,
                    total_classes=0,
                    attended_classes=0,
                    attendance_percentage=0,
                    guidance_notes=guidance
                )
            success = 'Marks saved successfully!'
        except Exception as e:
            error = 'Please enter valid marks!'
    return redirect(f'/academic/semester/{student_id}/{sem_number}/')

@login_required(login_url='/login')
def add_attendance(request, student_id, sem_number):
    """Add or update attendance for a subject"""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        subject = request.POST.get('subject_attendance')
        total_classes = request.POST.get('total_classes', 0)
        attended_classes = request.POST.get('attended_classes', 0)
        
        try:
            total_cls = int(total_classes) if total_classes else 0
            attended_cls = int(attended_classes) if attended_classes else 0
            
            if total_cls > 0:
                attendance_pct = round((attended_cls / total_cls) * 100)
            else:
                attendance_pct = 0
            
            # Check if marks already exist for this subject
            record = AcademicRecord.objects.filter(
                student=student,
                semester=sem_number,
                subject=subject
            ).first()
            
            if record:
                # Update existing record with attendance data
                record.total_classes = total_cls
                record.attended_classes = attended_cls
                record.attendance_percentage = attendance_pct
                record.save()
            else:
                # Marks haven't been added yet - create placeholder record
                # This will be replaced when marks are added
                AcademicRecord.objects.create(
                    student=student,
                    semester=sem_number,
                    subject=subject,
                    total_classes=total_cls,
                    attended_classes=attended_cls,
                    attendance_percentage=attendance_pct,
                    internal_marks=0,
                    external_marks=0,
                    assignments=0,
                    total_marks=0,
                    result='Incomplete'  # Mark as incomplete until marks are added
                )
        except Exception as e:
            pass
    
    return redirect(f'/academic/semester/{student_id}/{sem_number}/')

@login_required(login_url='/login')
def edit_academic(request, record_id):
    record = get_object_or_404(AcademicRecord, id=record_id)
    error = None
    success = None
    if request.method == 'POST':
        internal = request.POST.get('internal_marks')
        external = request.POST.get('external_marks')
        assignments = request.POST.get('assignments', record.assignments)
        try:
            internal_val = float(internal)
            external_val = float(external)
            assignments_val = float(assignments) if assignments else 0
            record.internal_marks = internal_val
            record.external_marks = external_val
            record.assignments = assignments_val
            # Recalculate total marks with all components
            record.total_marks = internal_val + external_val + assignments_val
            # Pass threshold: 60 marks out of 120 (50% - standard academic pass)
            record.result = 'Pass' if record.total_marks >= 60 else 'Fail'
            record.guidance_notes = request.POST.get('guidance_notes', '')
            record.save()
            success = 'Updated successfully!'
            return redirect(f'/academic/semester/{record.student.id}/{record.semester}/')
        except:
            error = 'Invalid marks!'
    return render(request, 'academic/edit.html', {'record': record, 'error': error, 'success': success})

@login_required(login_url='/login')
def delete_academic(request, record_id):
    record = get_object_or_404(AcademicRecord, id=record_id)
    student_id = record.student.id
    sem = record.semester
    if request.method == 'POST':
        record.delete()
    return redirect(f'/academic/semester/{student_id}/{sem}/')

@login_required(login_url='/login')
def add_project(request, student_id, sem_number):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        name = request.POST.get('project_name')
        file = request.FILES.get('project_file')
        Project.objects.create(student=student, semester=sem_number, name=name, file=file)
    return redirect(f'/academic/semester/{student_id}/{sem_number}/')

@login_required(login_url='/login')
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        # Update project name
        name = request.POST.get('project_name')
        if name:
            project.name = name
        
        # Update file if provided
        file = request.FILES.get('project_file')
        if file:
            # Delete old file if it exists
            if project.file:
                project.file.delete()
            project.file = file
        
        project.save()
    
    return redirect(f'/academic/semester/{project.student.id}/{project.semester}/')

@login_required(login_url='/login')
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    student_id = project.student.id
    sem = project.semester
    if request.method == 'POST':
        # Delete file from storage
        if project.file:
            project.file.delete()
        project.delete()
    return redirect(f'/academic/semester/{student_id}/{sem}/')

@login_required(login_url='/login')
def view_academic(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    records = AcademicRecord.objects.filter(student=student).order_by('semester', 'subject')
    return render(request, 'academic/view.html', {'student': student, 'records': records})