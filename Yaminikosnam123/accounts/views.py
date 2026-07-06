from meeting.models import Student
from academic.models import AcademicRecord
from activity.models import ActivityRecord
from career_guidance.models import CareerProfile, PlacementRecord
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm, SignUpForm


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            error = 'Please enter both username/email and password'
            return render(request, 'login.html', {'error': error})
        
        # Check if username is an email
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                error = 'Invalid username/email or password'
                return render(request, 'login.html', {'error': error})
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            error = 'Invalid username/email or password'
    
    return render(request, 'login.html', {'error': error})


def register_view(request):
    error = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')
            password = form.cleaned_data['password']
            
            try:
                # Create user
                user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password
                )
                user.save()
                
                # Create mentor profile
                from accounts.models import MentorProfile
                MentorProfile.objects.create(
                    user=user,
                    department=department,
                    phone=phone
                )
                
                # Redirect to login
                return redirect('/login/')
            except Exception as e:
                error = f'Error creating account: {str(e)}'
        else:
            # Get the first error message
            if form.errors:
                error = list(form.errors.values())[0][0]
    
    return render(request, 'register.html', {'error': error})


@login_required(login_url='/login')
def dashboard_view(request):
    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


def forgot_password_view(request):
    error = None
    success = None
    step = request.POST.get('step', '1')
    if request.method == 'POST':
        if step == '1':
            username = request.POST.get('username')
            department = request.POST.get('department')
            try:
                user = User.objects.get(username=username)
                from accounts.models import MentorProfile
                profile = MentorProfile.objects.get(user=user)
                if profile.department.lower() == department.lower():
                    return render(request, 'forgot_password.html', {'step': '2', 'username': username})
                else:
                    error = 'Department does not match our records!'
            except User.DoesNotExist:
                error = 'Username not found!'
            except:
                error = 'Verification failed. Please check your details!'
        elif step == '2':
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if not new_password or not confirm_password:
                error = 'Please fill all fields!'
                return render(request, 'forgot_password.html', {'step': '2', 'username': username, 'error': error})
            elif len(new_password) < 6:
                error = 'Password must be at least 6 characters!'
                return render(request, 'forgot_password.html', {'step': '2', 'username': username, 'error': error})
            elif new_password != confirm_password:
                error = 'Passwords do not match!'
                return render(request, 'forgot_password.html', {'step': '2', 'username': username, 'error': error})
            else:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    success = 'Password reset successfully! Please login with your new password.'
                    return render(request, 'forgot_password.html', {'step': '1', 'success': success})
                except:
                    error = 'Something went wrong. Please try again!'
    return render(request, 'forgot_password.html', {'step': '1', 'error': error, 'success': success})


@login_required(login_url='/login')
def analytics_view(request):
    from django.db.models import Count, Avg
    import datetime
    current_year = datetime.datetime.now().year
    selected_year = request.GET.get('year', str(current_year))
    
    all_students = Student.objects.filter(mentor=request.user)
    
    # Get available years from created_at and academic_year fields
    years_from_created = all_students.filter(created_at__isnull=False).dates('created_at', 'year')
    available_years = list(set([y.year for y in years_from_created]))
    if current_year not in available_years:
        available_years.append(current_year)
    available_years = sorted(set(available_years), reverse=True)
    
    # Filter students by year
    try:
        year_int = int(selected_year)
        if year_int == current_year:
            students = all_students
        else:
            students = all_students.filter(created_at__year=year_int)
    except ValueError:
        students = all_students
        selected_year = str(current_year)
    
    # ===== ANALYTICS DASHBOARD DATA =====
    total_students = students.count()
    total_degree = students.filter(graduation='Degree').count()
    total_pg = students.filter(graduation='PG').count()
    
    higher_studies = 0
    job_placement = 0
    undecided = 0
    total_placed = 0
    
    for student in students:
        try:
            profile = CareerProfile.objects.get(student=student)
            if profile.career_path == 'higher_studies':
                higher_studies += 1
            elif profile.career_path == 'job_placement':
                job_placement += 1
                placement = PlacementRecord.objects.filter(profile=profile).last()
                if placement and placement.placement_status == 'Placed':
                    total_placed += 1
            else:
                undecided += 1
        except CareerProfile.DoesNotExist:
            undecided += 1
    
    # Activity data
    activity_active = ActivityRecord.objects.filter(student__in=students, participation_status='Active').count()
    activity_completed = ActivityRecord.objects.filter(student__in=students, participation_status='Completed').count()
    activity_ongoing = ActivityRecord.objects.filter(student__in=students, participation_status='Ongoing').count()
    activity_not = ActivityRecord.objects.filter(student__in=students, participation_status='Not Participating').count()
    
    # Department and marks data
    dept_data = students.values('department').annotate(count=Count('id')).order_by('-count')
    marks_data = AcademicRecord.objects.filter(student__in=students).values('semester').annotate(avg=Avg('total_marks')).order_by('semester')
    marks_data = [{'semester': m['semester'], 'avg': round(m['avg'], 1)} for m in marks_data]
    
    # ===== SUCCESS ANALYTICS DATA =====
    # Student stages
    enrolled = students.filter(stage='enrolled').count()
    active = students.filter(stage='active').count()
    at_risk = students.filter(stage='at_risk').count()
    supply = students.filter(stage='supply').count()
    cleared = students.filter(stage='cleared').count()
    career_ready = students.filter(stage='career_ready').count()
    graduated = students.filter(stage='graduated').count()
    
    # Career outcomes
    placed = 0
    higher = 0
    still_looking = 0
    for student in students:
        try:
            profile = CareerProfile.objects.get(student=student)
            if profile.career_path == 'job_placement':
                p = PlacementRecord.objects.filter(profile=profile).last()
                if p and p.placement_status == 'Placed':
                    placed += 1
                else:
                    still_looking += 1
            elif profile.career_path == 'higher_studies':
                higher += 1
        except CareerProfile.DoesNotExist:
            pass
    
    successful = placed + higher + graduated
    success_rate = round((successful / total_students) * 100) if total_students > 0 else 0
    
    # Year-wise data for trends
    year_data = []
    for year in available_years:
        yr_students = all_students.filter(created_at__year=year)
        yr_total = yr_students.count()
        yr_placed = 0
        yr_higher = 0
        for s in yr_students:
            try:
                p = CareerProfile.objects.get(student=s)
                if p.career_path == 'job_placement':
                    pl = PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
                    yr_placed += pl
                elif p.career_path == 'higher_studies':
                    yr_higher += 1
            except CareerProfile.DoesNotExist:
                pass
        yr_success = yr_placed + yr_higher
        yr_rate = round((yr_success / yr_total) * 100) if yr_total > 0 else 0
        year_data.append({'year': year, 'total': yr_total, 'placed': yr_placed, 'higher': yr_higher, 'success_rate': yr_rate})
    
    # Degree vs PG placement data
    degree_students = students.filter(graduation='Degree')
    pg_students = students.filter(graduation='PG')
    degree_placed = 0
    pg_placed = 0
    for s in degree_students:
        try:
            p = CareerProfile.objects.get(student=s)
            if p.career_path == 'job_placement':
                degree_placed += PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
        except CareerProfile.DoesNotExist:
            pass
    for s in pg_students:
        try:
            p = CareerProfile.objects.get(student=s)
            if p.career_path == 'job_placement':
                pg_placed += PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
        except CareerProfile.DoesNotExist:
            pass
    
    return render(request, 'unified_analytics.html', {
        # Analytics Dashboard Data
        'total_students': total_students,
        'total_degree': total_degree,
        'total_pg': total_pg,
        'total_placed': total_placed,
        'higher_studies': higher_studies,
        'job_placement': job_placement,
        'undecided': undecided,
        'activity_active': activity_active,
        'activity_completed': activity_completed,
        'activity_ongoing': activity_ongoing,
        'activity_not': activity_not,
        'dept_data': dept_data,
        'marks_data': marks_data,
        
        # Success Analytics Data
        'enrolled': enrolled,
        'active': active,
        'at_risk': at_risk,
        'supply': supply,
        'cleared': cleared,
        'career_ready': career_ready,
        'graduated': graduated,
        'placed': placed,
        'higher': higher,
        'still_looking': still_looking,
        'success_rate': success_rate,
        'year_data': year_data,
        'degree_total': degree_students.count(),
        'pg_total': pg_students.count(),
        'degree_placed': degree_placed,
        'pg_placed': pg_placed,
        
        # Common Data
        'selected_year': selected_year,
        'available_years': available_years,
        'current_year': current_year,
    })


@login_required(login_url='/login')
def profile_edit_view(request):
    from accounts.models import MentorProfile
    error = None
    success = None
    
    try:
        profile = MentorProfile.objects.get(user=request.user)
    except MentorProfile.DoesNotExist:
        profile = MentorProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        department = request.POST.get('department', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        if not email:
            error = 'Email is required!'
        elif not department:
            error = 'Department is required!'
        else:
            try:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                request.user.save()
                
                profile.department = department
                profile.phone = phone
                profile.save()
                
                success = 'Profile updated successfully!'
            except Exception as e:
                error = f'Error updating profile: {str(e)}'
    
    context = {
        'profile': profile,
        'error': error,
        'success': success,
    }
    return render(request, 'profile_edit.html', context)


@login_required(login_url='/login')
def success_analytics(request):
    students_all = Student.objects.filter(mentor=request.user)
    all_years = students_all.values_list('academic_year', flat=True).distinct().order_by('academic_year')
    selected_year = request.GET.get('year', '2025-26')
    if selected_year == 'all':
        students = students_all
    else:
        students = students_all.filter(academic_year=selected_year)
    total = students.count()
    enrolled = students.filter(stage='enrolled').count()
    active = students.filter(stage='active').count()
    at_risk = students.filter(stage='at_risk').count()
    supply = students.filter(stage='supply').count()
    cleared = students.filter(stage='cleared').count()
    career_ready = students.filter(stage='career_ready').count()
    graduated = students.filter(stage='graduated').count()
    placed = 0
    higher = 0
    still_looking = 0
    for student in students:
        try:
            profile = CareerProfile.objects.get(student=student)
            if profile.career_path == 'job_placement':
                p = PlacementRecord.objects.filter(profile=profile).last()
                if p and p.placement_status == 'Placed':
                    placed += 1
                else:
                    still_looking += 1
            elif profile.career_path == 'higher_studies':
                higher += 1
        except CareerProfile.DoesNotExist:
            pass
    successful = placed + higher + graduated
    success_rate = round((successful / total) * 100) if total > 0 else 0
    year_data = []
    for year in all_years:
        yr_students = students_all.filter(academic_year=year)
        yr_total = yr_students.count()
        yr_placed = 0
        yr_higher = 0
        for s in yr_students:
            try:
                p = CareerProfile.objects.get(student=s)
                if p.career_path == 'job_placement':
                    pl = PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
                    yr_placed += pl
                elif p.career_path == 'higher_studies':
                    yr_higher += 1
            except CareerProfile.DoesNotExist:
                pass
        yr_success = yr_placed + yr_higher
        yr_rate = round((yr_success / yr_total) * 100) if yr_total > 0 else 0
        year_data.append({'year': year, 'total': yr_total, 'placed': yr_placed, 'higher': yr_higher, 'success_rate': yr_rate})
    degree_students = students.filter(graduation='Degree')
    pg_students = students.filter(graduation='PG')
    degree_placed = 0
    pg_placed = 0
    for s in degree_students:
        try:
            p = CareerProfile.objects.get(student=s)
            if p.career_path == 'job_placement':
                degree_placed += PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
        except CareerProfile.DoesNotExist:
            pass
    for s in pg_students:
        try:
            p = CareerProfile.objects.get(student=s)
            if p.career_path == 'job_placement':
                pg_placed += PlacementRecord.objects.filter(profile=p, placement_status='Placed').count()
        except CareerProfile.DoesNotExist:
            pass
    return render(request, 'success_analytics.html', {
        'total': total, 'enrolled': enrolled, 'active': active,
        'at_risk': at_risk, 'supply': supply, 'cleared': cleared,
        'career_ready': career_ready, 'graduated': graduated,
        'placed': placed, 'higher': higher, 'still_looking': still_looking,
        'success_rate': success_rate, 'all_years': all_years,
        'selected_year': selected_year, 'year_data': year_data,
        'degree_total': degree_students.count(), 'pg_total': pg_students.count(),
        'degree_placed': degree_placed, 'pg_placed': pg_placed,
    })