from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from .models import Faculty, Student, Review, Department, Course, Question, CourseReview
from .forms import StudentRegistrationForm, OTPVerificationForm, ReviewForm, CourseReviewForm
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
                # Check email backend configuration to provide helpful error message
                from django.conf import settings
                email_backend = getattr(settings, 'EMAIL_BACKEND', '')
                
                if 'console' in email_backend.lower():
                    messages.error(
                        request, 
                        'Email backend is set to console mode. OTP was printed to server console instead of being sent. '
                        'Please configure SMTP email settings in your .env file. See GMAIL_SETUP.md for instructions.'
                    )
                else:
                    messages.error(
                        request, 
                        'Failed to send OTP email. Please check your email configuration. '
                        'See GMAIL_SETUP.md for setup instructions or check server logs for details.'
                    )
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
            
            # Always set student reference (even for anonymous reviews)
            # The is_anonymous flag controls display, not data storage
            review.student = student
            
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


def course_list(request):
    """Course listing page with search and filter"""
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    courses = Course.objects.all()
    
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query)
        ).distinct()
    
    if department_filter:
        courses = courses.filter(department_id=department_filter)
    
    departments = Department.objects.all()
    
    # Add average rating to each course
    course_list_data = []
    for course in courses:
        course_list_data.append({
            'course': course,
            'avg_rating': course.average_rating(),
            'total_reviews': course.total_reviews()
        })
    
    context = {
        'course_list': course_list_data,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter,
    }
    return render(request, 'reviews/course_list.html', context)


def course_detail(request, course_id):
    """Course detail page with reviews"""
    course = get_object_or_404(Course, id=course_id)
    reviews = course.course_reviews.all()
    
    # Filter by tags if provided
    tag_filter = request.GET.get('tag', '')
    if tag_filter:
        reviews = [r for r in reviews if tag_filter in r.tags]
    
    context = {
        'course': course,
        'reviews': reviews,
        'avg_rating': course.average_rating(),
        'total_reviews': course.total_reviews(),
        'tag_filter': tag_filter,
        'available_tags': [tag[0] for tag in CourseReview.TAG_CHOICES],
    }
    return render(request, 'reviews/course_detail.html', context)


def submit_course_review(request):
    """Submit a course review (requires OTP verification)"""
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
    
    # Get course_id from URL parameter or POST data (if coming from course detail page)
    course_id = request.GET.get('course_id') or request.POST.get('course_id')
    selected_course = None
    
    if course_id:
        try:
            selected_course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        
        # If course is pre-selected, make it optional in the form
        if selected_course:
            form.fields['course'].required = False
        
        if form.is_valid():
            review = form.save(commit=False)
            
            # If course was pre-selected, use it (override form data)
            if selected_course:
                review.course = selected_course
            
            # Always set student reference (even for anonymous reviews)
            # The is_anonymous flag controls display, not data storage
            review.student = student
            
            # Convert tags list to JSON
            tags = form.cleaned_data.get('tags', [])
            review.tags = tags
            
            try:
                review.save()
                messages.success(request, 'Course review submitted successfully!')
                return redirect('course_detail', course_id=review.course.id)
            except Exception as e:
                messages.error(request, f'Error saving review: {str(e)}')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-populate form with selected course if available
        if selected_course:
            form = CourseReviewForm(initial={'course': selected_course})
            form.fields['course'].required = False
        else:
            form = CourseReviewForm()
    
    context = {
        'form': form,
        'student': student,
        'selected_course': selected_course,  # Pass to template to hide course field
    }
    return render(request, 'reviews/submit_course_review.html', context)