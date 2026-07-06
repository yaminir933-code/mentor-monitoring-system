from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from meeting.models import Student
from academic.models import AcademicRecord
from activity.models import ActivityRecord
from career_guidance.models import CareerProfile
from mentorapp.departments import DEPARTMENTS
from mentorapp.academic_years import ACADEMIC_YEARS
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@login_required(login_url='/login')
def students_home(request):
    selected_year = request.GET.get('year')

    # Filter students based on selected year
    if selected_year:
        students = Student.objects.filter(mentor=request.user, academic_year=selected_year).order_by('department')
    else:
        students = Student.objects.filter(mentor=request.user).order_by('department')

    # Filter by graduation type for the tabs
    degree_students = students.filter(graduation='Degree').order_by('department')
    pg_students = students.filter(graduation='PG').order_by('department')

    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        roll_number = request.POST.get('roll_number')
        graduation = request.POST.get('graduation')
        academic_year = request.POST.get('academic_year')

        if not name or not department or not roll_number or not graduation:
            error = 'All fields are required'
        else:
            Student.objects.create(
                mentor=request.user,
                name=name,
                department=department,
                roll_number=roll_number,
                graduation=graduation,
                academic_year=academic_year
            )
            return redirect('/students/')

    return render(request, 'students/home.html', {
        'students': students,
        'degree_students': degree_students,
        'pg_students': pg_students,
        'selected_year': selected_year,
        'error': error,
        'departments': DEPARTMENTS,
        'academic_years': ACADEMIC_YEARS,
    })

@login_required(login_url='/login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id, mentor=request.user)
    if request.method == 'POST':
        student.delete()
        return redirect('/students')
    return render(request, 'students/delete.html', {'student': student})

@login_required(login_url='/login')
def generate_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("Kasturba Gandhi Degree & PG College for Women", styles['Title']))
    elements.append(Paragraph("Mentor Monitoring System - Student Report", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Student Details", styles['Heading3']))
    student_data = [
        ['Name', student.name],
        ['Roll Number', student.roll_number],
        ['Department', student.department],
        ['Graduation', student.graduation],
        ['Academic Year', student.academic_year],
    ]
    t = Table(student_data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.lightblue),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Academic Records", styles['Heading3']))
    records = AcademicRecord.objects.filter(student=student).order_by('semester', 'subject')
    if records:
        academic_data = [['Semester', 'Subject', 'Internal', 'External', 'Total', 'Result', 'Attendance%']]
        for r in records:
            academic_data.append([f'Sem {r.semester}', r.subject, str(r.internal_marks), str(r.external_marks), str(r.total_marks), r.result, f'{r.attendance_percentage}%'])
        t2 = Table(academic_data, colWidths=[60, 120, 60, 60, 60, 50, 80])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t2)
    else:
        elements.append(Paragraph("No academic records found.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Activity Records", styles['Heading3']))
    activities = ActivityRecord.objects.filter(student=student).order_by('-date')
    if activities:
        activity_data = [['Activity Type', 'Activity Name', 'Date', 'Status', 'Achievement']]
        for a in activities:
            activity_data.append([a.activity_type, a.activity_name, str(a.date), a.participation_status, a.achievement or '-'])
        t3 = Table(activity_data, colWidths=[90, 130, 70, 90, 110])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.orange),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t3)
    else:
        elements.append(Paragraph("No activity records found.", styles['Normal']))
    doc.build(elements)
    return response

@login_required(login_url='/login')
def pipeline_view(request):
    students = Student.objects.filter(mentor=request.user)
    stage_info = [
        {'key': 'enrolled', 'name': 'Enrolled', 'icon': '📝', 'color': '#42A5F5'},
        {'key': 'active', 'name': 'Active', 'icon': '✅', 'color': '#66BB6A'},
        {'key': 'at_risk', 'name': 'At Risk', 'icon': '⚠️', 'color': '#FFA726'},
        {'key': 'supply', 'name': 'Supply/Arrear', 'icon': '❌', 'color': '#EF5350'},
        {'key': 'cleared', 'name': 'Cleared', 'icon': '🎯', 'color': '#26C6DA'},
        {'key': 'career_ready', 'name': 'Career Ready', 'icon': '💼', 'color': '#AB47BC'},
        {'key': 'graduated', 'name': 'Graduated', 'icon': '🎓', 'color': '#F9A825'},
    ]
    for s in stage_info:
        s['students'] = students.filter(stage=s['key'])
        s['count'] = s['students'].count()
    total_degree = students.filter(graduation='Degree').count()
    total_pg = students.filter(graduation='PG').count()
    return render(request, 'students/pipeline.html', {
        'stages': stage_info,
        'total_degree': total_degree,
        'total_pg': total_pg,
    })

@login_required(login_url='/login')
def update_stage(request, student_id):
    student = get_object_or_404(Student, id=student_id, mentor=request.user)
    if request.method == 'POST':
        student.stage = request.POST.get('stage')
        student.save()
    return redirect('/students/pipeline/')