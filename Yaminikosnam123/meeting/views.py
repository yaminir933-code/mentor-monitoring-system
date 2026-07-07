from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Meeting
from datetime import date

@login_required(login_url='/login')
def meeting_home(request):
    from mentorapp.academic_years import ACADEMIC_YEARS
    selected_year = request.GET.get('year', '')

    # Only show this mentor's students, filtered by year if selected
    students_qs = Student.objects.filter(mentor=request.user).order_by('department', 'name')
    if selected_year:
        students_qs = students_qs.filter(academic_year=selected_year)

    summary = []
    today = date.today()
    for student in students_qs:
        meetings = Meeting.objects.filter(student=student).order_by('-date')
        total = meetings.count()
        missed = 0
        last_meeting = None
        days_since = None
        if meetings.exists():
            last_meeting = meetings.first().date
            days_since = (today - last_meeting).days
            if days_since > 14:
                missed = 1
        regularity = round((total / (total + missed)) * 100) if total > 0 else 0
        summary.append({
            'student': student,
            'total': total,
            'missed': missed,
            'regularity': regularity,
            'last_meeting': last_meeting,
            'days_since': days_since,
        })
    return render(request, 'meeting/home.html', {
        'summary': summary,
        'selected_year': selected_year,
        'academic_years': ACADEMIC_YEARS,
    })

@login_required(login_url='/login')
def add_meeting(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    error = None
    if request.method == 'POST':
        date_val = request.POST['date']
        meeting_type = request.POST['meeting_type']
        discussion = request.POST['discussion']
        guidance = request.POST['guidance']
        follow_up = request.POST['follow_up']
        if not date_val or not discussion:
            error = 'All fields are required'
        else:
            Meeting.objects.create(
                student=student,
                date=date_val,
                meeting_type=meeting_type,
                discussion=discussion,
                guidance=guidance,
                follow_up=follow_up
            )
            return redirect(f'/meeting/view/{student_id}')
    return render(request, 'meeting/add.html', {'student': student, 'error': error})

@login_required(login_url='/login')
def view_meetings(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    meetings = Meeting.objects.filter(student=student).order_by('-date')
    total = meetings.count()
    today = date.today()
    missed = 0
    if meetings.exists():
        last = meetings.first().date
        gap = (today - last).days
        if gap > 14:
            missed = 1
    regularity = round((total / (total + missed)) * 100) if total > 0 else 0
    return render(request, 'meeting/view.html', {
        'student': student,
        'meetings': meetings,
        'total': total,
        'regularity': regularity,
        'missed': missed
    })

@login_required(login_url='/login')
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    error = None
    if request.method == 'POST':
        meeting.date = request.POST['date']
        meeting.meeting_type = request.POST['meeting_type']
        meeting.discussion = request.POST['discussion']
        meeting.guidance = request.POST['guidance']
        meeting.follow_up = request.POST['follow_up']
        meeting.save()
        return redirect(f'/meeting/view/{meeting.student.id}')
    return render(request, 'meeting/edit.html', {'meeting': meeting, 'error': error})

@login_required(login_url='/login')
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    student_id = meeting.student.id
    if request.method == 'POST':
        meeting.delete()
        return redirect(f'/meeting/view/{student_id}')
    return render(request, 'meeting/delete.html', {'meeting': meeting})