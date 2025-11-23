from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Faculty, Student, Review, Department, Course, Question
from .forms import StudentRegistrationForm, OTPVerificationForm, ReviewForm
from .utils import generate_otp, send_otp_email


def home(request):
    """Home page with faculty listing and search"""
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    faculties = Faculty.objects.all()
    
    if search_query:
        faculties = faculties.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(courses__name__icontains=search_query) |
            Q(courses__code__icontains=search_query)
        ).distinct()
    
    if department_filter:
        faculties = faculties.filter(department_id=department_filter)
    
    departments = Department.objects.all()
    
    # Add average rating to each faculty
    faculty_list = []
    for faculty in faculties:
        faculty_list.append({
            'faculty': faculty,
            'avg_rating': faculty.average_rating(),
            'total_reviews': faculty.total_reviews()
        })
    
    context = {
        'faculty_list': faculty_list,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter,
    }
    return render(request, 'reviews/home.html', context)


def student_register(request):
    """Student registration with OTP generation"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            # Get or create student
            student, created = Student.objects.get_or_create(
                student_id=email,
                defaults={'name': name}
            )
            
            # Generate and send OTP
            otp = generate_otp()
            student.last_otp = otp
            student.otp_created_at = timezone.now()
            student.save()
            
            # Send OTP via email
            if send_otp_email(email, otp):
                # Store student email in session for verification
                request.session['student_email'] = email
                messages.success(request, f'OTP has been sent to {email}. Please check your email.')
                return redirect('verify_otp')
            else:
                messages.error(request, 'Failed to send OTP. Please try again.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'reviews/register.html', {'form': form})


def verify_otp(request):
    """Verify OTP and create session"""
    student_email = request.session.get('student_email')
    
    if not student_email:
        messages.error(request, 'Please register first.')
        return redirect('register')
    
    try:
        student = Student.objects.get(student_id=student_email)
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('register')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            # Verify OTP
            if student.last_otp == otp:
                if student.is_otp_valid():
                    # Mark email as verified
                    student.email_verified = True
                    student.save()
                    
                    # Create session
                    request.session['verified_student_id'] = student.id
                    request.session['student_name'] = student.name
                    
                    messages.success(request, f'Welcome, {student.name}! You are now verified.')
                    return redirect('home')
                else:
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('register')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'reviews/verify_otp.html', {
        'form': form,
        'student_email': student_email
    })


def faculty_detail(request, faculty_id):
    """Faculty detail page with reviews"""
    faculty = get_object_or_404(Faculty, id=faculty_id)
    reviews = faculty.reviews.all()
    
    # Filter by tags if provided
    tag_filter = request.GET.get('tag', '')
    if tag_filter:
        reviews = [r for r in reviews if tag_filter in r.tags]
    
    context = {
        'faculty': faculty,
        'reviews': reviews,
        'avg_rating': faculty.average_rating(),
        'total_reviews': faculty.total_reviews(),
        'tag_filter': tag_filter,
        'available_tags': [tag[0] for tag in Review.TAG_CHOICES],
    }
    return render(request, 'reviews/faculty_detail.html', context)


def submit_review(request):
    """Submit a review (requires OTP verification)"""
    # Check if student is verified
    verified_student_id = request.session.get('verified_student_id')
    
    if not verified_student_id:
        messages.error(request, 'Please verify your email first to submit a review.')
        return redirect('register')
    
    try:
        student = Student.objects.get(id=verified_student_id)
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('register')
    
    # Get faculty_id from URL parameter or POST data (if coming from faculty detail page)
    faculty_id = request.GET.get('faculty_id') or request.POST.get('faculty_id')
    selected_faculty = None
    
    if faculty_id:
        try:
            selected_faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            messages.error(request, 'Faculty not found.')
            return redirect('home')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        # If faculty is pre-selected, make it optional in the form
        if selected_faculty:
            form.fields['faculty'].required = False
        
        if form.is_valid():
            review = form.save(commit=False)
            
            # If faculty was pre-selected, use it (override form data)
            if selected_faculty:
                review.faculty = selected_faculty
            
            # Set student (or null if anonymous)
            if not review.is_anonymous:
                review.student = student
            else:
                review.student = None
            
            # Convert tags list to JSON
            tags = form.cleaned_data.get('tags', [])
            review.tags = tags
            
            try:
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('faculty_detail', faculty_id=review.faculty.id)
            except Exception as e:
                messages.error(request, f'Error saving review: {str(e)}')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-populate form with selected faculty if available
        if selected_faculty:
            form = ReviewForm(initial={'faculty': selected_faculty})
            form.fields['faculty'].required = False
        else:
            form = ReviewForm()
    
    context = {
        'form': form,
        'student': student,
        'selected_faculty': selected_faculty,  # Pass to template to hide faculty field
    }
    return render(request, 'reviews/submit_review.html', context)


def search_reviews(request):
    """Search and filter reviews"""
    search_query = request.GET.get('search', '')
    faculty_filter = request.GET.get('faculty', '')
    course_filter = request.GET.get('course', '')
    department_filter = request.GET.get('department', '')
    tag_filter = request.GET.get('tag', '')
    
    reviews = Review.objects.all()
    
    if search_query:
        reviews = reviews.filter(
            Q(description__icontains=search_query) |
            Q(faculty__name__icontains=search_query)
        )
    
    if faculty_filter:
        reviews = reviews.filter(faculty_id=faculty_filter)
    
    if course_filter:
        reviews = reviews.filter(faculty__courses__id=course_filter)
    
    if department_filter:
        reviews = reviews.filter(faculty__department_id=department_filter)
    
    if tag_filter:
        reviews = [r for r in reviews if tag_filter in r.tags]
    
    context = {
        'reviews': reviews,
        'faculties': Faculty.objects.all(),
        'courses': Course.objects.all(),
        'departments': Department.objects.all(),
        'available_tags': [tag[0] for tag in Review.TAG_CHOICES],
        'search_query': search_query,
        'faculty_filter': faculty_filter,
        'course_filter': course_filter,
        'department_filter': department_filter,
        'tag_filter': tag_filter,
    }
    return render(request, 'reviews/search_results.html', context)


def logout_view(request):
    """Logout and clear session"""
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')
