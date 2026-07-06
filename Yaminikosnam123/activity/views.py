from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from meeting.models import Student
from .models import ActivityRecord

@login_required(login_url='/login')
def activity_home(request):
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

    student_activity_count = []
    type_counts = {}
    status_counts = {'Active': 0, 'Completed': 0, 'Ongoing': 0, 'Not Participating': 0}

    for student in students:
        activities = ActivityRecord.objects.filter(student=student)
        student_activity_count.append({'name': student.name, 'count': activities.count()})
        for a in activities:
            type_counts[a.activity_type] = type_counts.get(a.activity_type, 0) + 1
            if a.participation_status in status_counts:
                status_counts[a.participation_status] += 1

    return render(request, 'activity/home.html', {
        'students': students,
        'student_activity_count': student_activity_count,
        'type_labels': list(type_counts.keys()),
        'type_values': list(type_counts.values()),
        'status_counts': status_counts,
        'selected_year': selected_year,
        'all_years': all_years,
    })

    # Chart data
    student_activity_count = []
    type_counts = {}
    status_counts = {'Active': 0, 'Completed': 0, 'Ongoing': 0, 'Not Participating': 0}

    for student in students:
        activities = ActivityRecord.objects.filter(student=student)
        student_activity_count.append({'name': student.name, 'count': activities.count()})
        for a in activities:
            type_counts[a.activity_type] = type_counts.get(a.activity_type, 0) + 1
            if a.participation_status in status_counts:
                status_counts[a.participation_status] += 1

    return render(request, 'activity/home.html', {
        'students': students,
        'student_activity_count': student_activity_count,
        'type_labels': list(type_counts.keys()),
        'type_values': list(type_counts.values()),
        'status_counts': status_counts,
    })

@login_required(login_url='/login')
def add_activity(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    error = None
    success = None
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        activity_name = request.POST.get('activity_name')
        date = request.POST.get('date')
        participation_status = request.POST.get('participation_status')
        achievement = request.POST.get('achievement', '')
        score = request.POST.get('score', '')
        reason = request.POST.get('reason_not_participating', '')
        skills = request.POST.get('skills_gained', '')
        guidance = request.POST.get('guidance_notes', '')
        encouragement = request.POST.get('encouragement_plan', '')
        upload_file = request.FILES.get('upload_file')
        if not activity_type or not activity_name or not date:
            error = 'Please fill all required fields!'
        else:
            ActivityRecord.objects.create(
                student=student,
                activity_type=activity_type,
                activity_name=activity_name,
                date=date,
                participation_status=participation_status,
                achievement=achievement,
                score=score,
                reason_not_participating=reason,
                skills_gained=skills,
                guidance_notes=guidance,
                encouragement_plan=encouragement,
                upload_file=upload_file
            )
            success = 'Activity record saved successfully!'
    return render(request, 'activity/add.html', {'student': student, 'error': error, 'success': success})

@login_required(login_url='/login')
def view_activity(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    records = ActivityRecord.objects.filter(student=student).order_by('-date')
    not_participating = records.filter(participation_status='Not Participating').count()
    return render(request, 'activity/view.html', {
        'student': student,
        'records': records,
        'not_participating': not_participating
    })

@login_required(login_url='/login')
def edit_activity(request, record_id):
    record = get_object_or_404(ActivityRecord, id=record_id)
    error = None
    success = None
    if request.method == 'POST':
        record.activity_type = request.POST.get('activity_type')
        record.activity_name = request.POST.get('activity_name')
        record.date = request.POST.get('date')
        record.participation_status = request.POST.get('participation_status')
        record.achievement = request.POST.get('achievement', '')
        record.score = request.POST.get('score', '')
        record.reason_not_participating = request.POST.get('reason_not_participating', '')
        record.skills_gained = request.POST.get('skills_gained', '')
        record.guidance_notes = request.POST.get('guidance_notes', '')
        record.encouragement_plan = request.POST.get('encouragement_plan', '')
        if request.FILES.get('upload_file'):
            record.upload_file = request.FILES.get('upload_file')
        record.save()
        success = 'Updated successfully!'
        return redirect(f'/activity/view/{record.student.id}/')
    return render(request, 'activity/edit.html', {'record': record, 'error': error, 'success': success})

@login_required(login_url='/login')
def delete_activity(request, record_id):
    record = get_object_or_404(ActivityRecord, id=record_id)
    student_id = record.student.id
    if request.method == 'POST':
        record.delete()
        return redirect(f'/activity/view/{student_id}/')
    return render(request, 'activity/delete.html', {'record': record})