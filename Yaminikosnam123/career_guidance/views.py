from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from meeting.models import Student
from .models import CareerProfile, HigherStudiesRecord, PlacementRecord

@login_required(login_url='/login')
def career_home(request):
    from mentorapp.academic_years import ACADEMIC_YEARS
    selected_year = request.GET.get('year', '')

    # Only show this mentor's students
    students_qs = Student.objects.filter(mentor=request.user).order_by('department', 'name')
    if selected_year:
        students_qs = students_qs.filter(academic_year=selected_year)

    student_data = []
    for student in students_qs:
        try:
            profile = CareerProfile.objects.get(student=student)
        except CareerProfile.DoesNotExist:
            profile = None
        student_data.append({'student': student, 'profile': profile})

    return render(request, 'career/home.html', {
        'student_data': student_data,
        'selected_year': selected_year,
        'academic_years': ACADEMIC_YEARS,
    })

@login_required(login_url='/login')
def career_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    try:
        profile = CareerProfile.objects.get(student=student)
    except CareerProfile.DoesNotExist:
        profile = None
    higher_records = HigherStudiesRecord.objects.filter(profile=profile) if profile else []
    placement_records = PlacementRecord.objects.filter(profile=profile) if profile else []
    return render(request, 'career/profile.html', {
        'student': student,
        'profile': profile,
        'higher_records': higher_records,
        'placement_records': placement_records,
    })

@login_required(login_url='/login')
def set_career_path(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    error = None
    success = None
    if request.method == 'POST':
        career_path = request.POST.get('career_path')
        mobile_number = request.POST.get('mobile_number', '')
        profile, created = CareerProfile.objects.get_or_create(student=student)
        profile.career_path = career_path
        profile.mobile_number = mobile_number
        profile.save()
        success = f'Career path set successfully!'
        return redirect(f'/career/profile/{student_id}')
    try:
        profile = CareerProfile.objects.get(student=student)
    except CareerProfile.DoesNotExist:
        profile = None
    return render(request, 'career/set_path.html', {
        'student': student,
        'profile': profile,
        'error': error,
        'success': success
    })

@login_required(login_url='/login')
def add_higher_studies(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    profile, created = CareerProfile.objects.get_or_create(student=student)
    error = None
    success = None
    if request.method == 'POST':
        goal_type = request.POST.get('goal_type')
        interest_area = request.POST.get('interest_area')
        target_institution = request.POST.get('target_institution', '')
        preparation_level = request.POST.get('preparation_level', 0)
        progress_status = request.POST.get('progress_status')
        exam_score = request.POST.get('exam_score', '')
        guidance_plan = request.POST.get('guidance_plan', '')
        resources_provided = request.POST.get('resources_provided', '')
        if not goal_type or not interest_area:
            error = 'Please fill all required fields!'
        else:
            HigherStudiesRecord.objects.create(
                profile=profile,
                goal_type=goal_type,
                interest_area=interest_area,
                target_institution=target_institution,
                preparation_level=int(preparation_level),
                progress_status=progress_status,
                exam_score=exam_score,
                guidance_plan=guidance_plan,
                resources_provided=resources_provided
            )
            success = 'Higher studies record saved!'
            return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/add_higher.html', {
        'student': student,
        'error': error,
        'success': success
    })

@login_required(login_url='/login')
def add_placement(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    profile, created = CareerProfile.objects.get_or_create(student=student)
    error = None
    success = None
    if request.method == 'POST':
        placement_office_visits = request.POST.get('placement_office_visits', 0)
        interviews_attended = request.POST.get('interviews_attended', 0)
        interviews_cleared = request.POST.get('interviews_cleared', 0)
        placement_status = request.POST.get('placement_status')
        company_name = request.POST.get('company_name', '')
        job_role = request.POST.get('job_role', '')
        salary = request.POST.get('salary', '')
        job_location = request.POST.get('job_location', '')
        offer_date = request.POST.get('offer_date', None)
        guidance_notes = request.POST.get('guidance_notes', '')
        if not placement_status:
            error = 'Please select placement status!'
        else:
            PlacementRecord.objects.create(
                profile=profile,
                placement_office_visits=int(placement_office_visits),
                interviews_attended=int(interviews_attended),
                interviews_cleared=int(interviews_cleared),
                placement_status=placement_status,
                company_name=company_name,
                job_role=job_role,
                salary=salary,
                job_location=job_location,
                offer_date=offer_date if offer_date else None,
                guidance_notes=guidance_notes
            )
            success = 'Placement record saved!'
            return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/add_placement.html', {
        'student': student,
        'error': error,
        'success': success
    })

@login_required(login_url='/login')
def career_report(request):
    students = Student.objects.filter(mentor=request.user)
    total = students.count()
    placed = 0
    higher_studies = 0
    still_looking = 0
    undecided = 0
    report_data = []
    for student in students:
        try:
            profile = CareerProfile.objects.get(student=student)
            if profile.career_path == 'job_placement':
                placement = PlacementRecord.objects.filter(profile=profile).last()
                if placement and placement.placement_status == 'Placed':
                    placed += 1
                else:
                    still_looking += 1
            elif profile.career_path == 'higher_studies':
                higher_studies += 1
            else:
                undecided += 1
            report_data.append({'student': student, 'profile': profile})
        except CareerProfile.DoesNotExist:
            undecided += 1
            report_data.append({'student': student, 'profile': None})
    return render(request, 'career/report.html', {
        'report_data': report_data,
        'total': total,
        'placed': placed,
        'higher_studies': higher_studies,
        'still_looking': still_looking,
        'undecided': undecided,
    })

@login_required(login_url='/login')
def delete_higher(request, record_id):
    record = get_object_or_404(HigherStudiesRecord, id=record_id)
    student_id = record.profile.student.id
    if request.method == 'POST':
        record.delete()
        return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/delete.html', {'record': record, 'type': 'higher'})

@login_required(login_url='/login')
def delete_placement(request, record_id):
    record = get_object_or_404(PlacementRecord, id=record_id)
    student_id = record.profile.student.id
    if request.method == 'POST':
        record.delete()
        return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/delete.html', {'record': record, 'type': 'placement'})

@login_required(login_url='/login')
def edit_higher(request, record_id):
    record = get_object_or_404(HigherStudiesRecord, id=record_id)
    student_id = record.profile.student.id
    if request.method == 'POST':
        record.goal_type = request.POST.get('goal_type')
        record.interest_area = request.POST.get('interest_area')
        record.target_institution = request.POST.get('target_institution', '')
        record.preparation_level = int(request.POST.get('preparation_level', 0))
        record.progress_status = request.POST.get('progress_status')
        record.exam_score = request.POST.get('exam_score', '')
        record.guidance_plan = request.POST.get('guidance_plan', '')
        record.resources_provided = request.POST.get('resources_provided', '')
        record.save()
        return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/edit_higher.html', {'record': record})

@login_required(login_url='/login')
def edit_placement(request, record_id):
    record = get_object_or_404(PlacementRecord, id=record_id)
    student_id = record.profile.student.id
    if request.method == 'POST':
        record.placement_office_visits = int(request.POST.get('placement_office_visits', 0))
        record.interviews_attended = int(request.POST.get('interviews_attended', 0))
        record.interviews_cleared = int(request.POST.get('interviews_cleared', 0))
        record.placement_status = request.POST.get('placement_status')
        record.company_name = request.POST.get('company_name', '')
        record.job_role = request.POST.get('job_role', '')
        record.salary = request.POST.get('salary', '')
        record.job_location = request.POST.get('job_location', '')
        record.guidance_notes = request.POST.get('guidance_notes', '')
        record.save()
        return redirect(f'/career/profile/{student_id}')
    return render(request, 'career/edit_placement.html', {'record': record})

@login_required(login_url='/login')
def delete_career_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    try:
        profile = CareerProfile.objects.get(student=student)
        if request.method == 'POST':
            profile.delete()
            return redirect('/career/')
    except CareerProfile.DoesNotExist:
        pass
    return redirect('/career/')
