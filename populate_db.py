"""
Database Population Script for ClassCritic
Generates realistic fake data for all models using Faker
"""

import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classcritic.settings')
django.setup()

from faker import Faker
from django.utils import timezone
from reviews.models import Department, Course, Faculty, Student, Question, Review, CourseReview

# Initialize Faker
fake = Faker()

# Configuration
CLEAR_EXISTING_DATA = True
NUM_DEPARTMENTS = 6
NUM_COURSES_PER_DEPT = 5
NUM_FACULTY_PER_DEPT = 4
NUM_STUDENTS = 50
NUM_QUESTIONS = 8
NUM_FACULTY_REVIEWS = 100
NUM_COURSE_REVIEWS = 80

# Bangladeshi university context
DEPARTMENT_NAMES = [
    "Computer Science & Engineering",
    "Business Administration",
    "Electrical & Electronic Engineering",
    "English & Humanities",
    "Mathematics & Natural Sciences",
    "Law",
    "Economics",
    "Civil Engineering"
]

DESIGNATIONS = [
    "Professor",
    "Associate Professor",
    "Assistant Professor",
    "Senior Lecturer",
    "Lecturer"
]

COURSE_PREFIXES = {
    "Computer Science & Engineering": "CSE",
    "Business Administration": "BBA",
    "Electrical & Electronic Engineering": "EEE",
    "English & Humanities": "ENG",
    "Mathematics & Natural Sciences": "MATH",
    "Law": "LAW",
    "Economics": "ECO",
    "Civil Engineering": "CEE"
}

COURSE_NAMES = {
    "CSE": ["Data Structures", "Algorithms", "Database Systems", "Operating Systems", "Computer Networks", 
            "Software Engineering", "Artificial Intelligence", "Machine Learning", "Web Development", "Mobile App Development"],
    "BBA": ["Principles of Management", "Marketing Management", "Financial Accounting", "Business Statistics", 
            "Organizational Behavior", "Human Resource Management", "Strategic Management", "Entrepreneurship"],
    "EEE": ["Circuit Analysis", "Digital Electronics", "Signals and Systems", "Electromagnetic Theory", 
            "Power Systems", "Control Systems", "Communication Engineering", "Microprocessors"],
    "ENG": ["English Composition", "British Literature", "American Literature", "Creative Writing", 
            "Linguistics", "World Literature", "Technical Writing", "Public Speaking"],
    "MATH": ["Calculus I", "Calculus II", "Linear Algebra", "Differential Equations", "Statistics", 
             "Discrete Mathematics", "Numerical Methods", "Complex Analysis"],
    "LAW": ["Constitutional Law", "Criminal Law", "Contract Law", "Corporate Law", 
            "International Law", "Human Rights Law", "Environmental Law", "Cyber Law"],
    "ECO": ["Microeconomics", "Macroeconomics", "Econometrics", "Development Economics", 
            "International Economics", "Public Finance", "Monetary Economics", "Game Theory"],
    "CEE": ["Engineering Mechanics", "Structural Analysis", "Geotechnical Engineering", "Transportation Engineering", 
            "Environmental Engineering", "Construction Management", "Hydraulics", "Surveying"]
}

REVIEW_QUESTIONS = [
    "How would you rate the teaching quality?",
    "How helpful was the faculty outside of class?",
    "How fair was the grading system?",
    "Would you recommend this faculty to other students?",
    "How well did the faculty explain complex concepts?",
    "How responsive was the faculty to student questions?",
    "How organized were the lectures?",
    "How engaging were the class sessions?"
]

COURSE_REVIEW_QUESTIONS = [
    "How would you rate the course content?",
    "How useful was this course for your career?",
    "How well-structured was the course?",
    "Would you recommend this course to other students?",
    "How challenging was the course material?",
    "How relevant was the course to real-world applications?",
    "How clear were the course objectives?",
    "How well did the course meet your expectations?"
]

FACULTY_REVIEW_TAGS = ['Good', 'Better', 'Best', 'Worst', 'Nice', 'Student Friendly']
COURSE_REVIEW_TAGS = ['Good', 'Better', 'Best', 'Worst', 'Nice', 'Easy', 'Difficult', 'Interesting', 'Useful']

POSITIVE_REVIEWS = [
    "Excellent teaching style and very approachable. Always willing to help students.",
    "Great professor! Makes complex topics easy to understand.",
    "Very knowledgeable and passionate about the subject. Highly recommended!",
    "Clear explanations and fair grading. One of the best instructors I've had.",
    "Engaging lectures and helpful feedback. Really cares about student success.",
    "Outstanding teacher with great communication skills.",
    "Very supportive and encourages critical thinking.",
    "Fantastic instructor! Makes learning enjoyable and interactive.",
    "Well-organized classes and provides excellent resources.",
    "Inspiring teacher who motivates students to excel."
]

NEGATIVE_REVIEWS = [
    "Teaching style needs improvement. Often unclear in explanations.",
    "Grading seems inconsistent and sometimes unfair.",
    "Not very responsive to student questions or concerns.",
    "Lectures can be boring and hard to follow.",
    "Expects too much without providing adequate guidance.",
    "Communication could be better. Sometimes difficult to reach.",
    "Course material is outdated and not very relevant.",
    "Not very organized. Deadlines and requirements often change.",
    "Doesn't seem very interested in teaching.",
    "Too strict and not very understanding of student situations."
]

NEUTRAL_REVIEWS = [
    "Decent instructor. Nothing exceptional but gets the job done.",
    "Average teaching quality. Could be better with more engagement.",
    "Fair grading but lectures could be more interesting.",
    "Okay professor. Some topics are explained well, others not so much.",
    "Standard teaching approach. Nothing particularly memorable.",
    "Acceptable but there's room for improvement.",
    "Does the basics right but lacks innovation in teaching methods.",
    "Reasonable instructor with average communication skills."
]

COURSE_POSITIVE_REVIEWS = [
    "Excellent course! Learned a lot of practical skills.",
    "Very well-structured and informative. Highly recommend!",
    "Great course content with real-world applications.",
    "Challenging but rewarding. Really helped me grow.",
    "One of the best courses I've taken. Very useful!",
    "Comprehensive coverage of topics with good resources.",
    "Interesting and engaging course material.",
    "Perfect balance of theory and practice."
]

COURSE_NEGATIVE_REVIEWS = [
    "Course content is outdated and not very relevant.",
    "Too difficult without proper support materials.",
    "Not well-organized. Objectives were unclear.",
    "Boring lectures and uninteresting assignments.",
    "Expected more practical applications.",
    "Course load is too heavy for the credit hours.",
    "Materials are hard to understand without better explanations.",
    "Not worth the time and effort required."
]

COURSE_NEUTRAL_REVIEWS = [
    "Decent course. Covers the basics adequately.",
    "Average course content. Nothing special.",
    "Okay course but could be more engaging.",
    "Standard curriculum. Gets the job done.",
    "Fair course with room for improvement.",
    "Acceptable but not particularly memorable."
]


def clear_data():
    """Clear all existing data from the database"""
    print("Clearing existing data...")
    CourseReview.objects.all().delete()
    Review.objects.all().delete()
    Question.objects.all().delete()
    Student.objects.all().delete()
    Faculty.objects.all().delete()
    Course.objects.all().delete()
    Department.objects.all().delete()
    print("[OK] Existing data cleared")


def create_departments():
    """Create departments"""
    print("\nCreating departments...")
    departments = []
    for i in range(min(NUM_DEPARTMENTS, len(DEPARTMENT_NAMES))):
        dept = Department.objects.create(name=DEPARTMENT_NAMES[i])
        departments.append(dept)
        print(f"  [OK] Created: {dept.name}")
    return departments


def create_courses(departments):
    """Create courses for each department"""
    print("\nCreating courses...")
    courses = []
    for dept in departments:
        prefix = COURSE_PREFIXES.get(dept.name, "GEN")
        course_names = COURSE_NAMES.get(prefix, ["General Course"])
        
        num_courses = min(NUM_COURSES_PER_DEPT, len(course_names))
        for i in range(num_courses):
            course_code = f"{prefix}{random.randint(100, 499)}"
            # Ensure unique course code
            while Course.objects.filter(code=course_code).exists():
                course_code = f"{prefix}{random.randint(100, 499)}"
            
            course = Course.objects.create(
                name=course_names[i],
                code=course_code,
                department=dept
            )
            courses.append(course)
            print(f"  [OK] Created: {course.code} - {course.name}")
    return courses


def create_faculty(departments, courses):
    """Create faculty members and assign courses"""
    print("\nCreating faculty members...")
    faculty_list = []
    
    for dept in departments:
        dept_courses = [c for c in courses if c.department == dept]
        
        for i in range(NUM_FACULTY_PER_DEPT):
            name = fake.name()
            # Create email from name
            email_name = name.lower().replace(' ', '.').replace("'", "")
            email = f"{email_name}@ewubd.edu"
            
            # Ensure unique email
            counter = 1
            while Faculty.objects.filter(email=email).exists():
                email = f"{email_name}{counter}@ewubd.edu"
                counter += 1
            
            faculty = Faculty.objects.create(
                name=name,
                email=email,
                designation=random.choice(DESIGNATIONS),
                department=dept
            )
            
            # Assign 2-4 random courses from the department
            num_courses = random.randint(2, min(4, len(dept_courses)))
            assigned_courses = random.sample(dept_courses, num_courses)
            faculty.courses.set(assigned_courses)
            
            faculty_list.append(faculty)
            print(f"  [OK] Created: {faculty.name} ({faculty.designation})")
    
    return faculty_list


def create_students():
    """Create verified students"""
    print("\nCreating students...")
    students = []
    
    for i in range(NUM_STUDENTS):
        name = fake.name()
        # Create student ID (email)
        student_number = f"{random.randint(2019, 2024)}{random.randint(1, 3)}{random.randint(100, 999):03d}"
        student_id = f"{student_number}@std.ewubd.edu"
        
        # Ensure unique student ID
        while Student.objects.filter(student_id=student_id).exists():
            student_number = f"{random.randint(2019, 2024)}{random.randint(1, 3)}{random.randint(100, 999):03d}"
            student_id = f"{student_number}@std.ewubd.edu"
        
        student = Student.objects.create(
            name=name,
            student_id=student_id,
            email_verified=True  # All students are verified
        )
        students.append(student)
        
        if (i + 1) % 10 == 0:
            print(f"  [OK] Created {i + 1} students...")
    
    print(f"  [OK] Total students created: {len(students)}")
    return students


def create_questions():
    """Create review questions"""
    print("\nCreating review questions...")
    questions = []
    
    # Create faculty review questions
    for question_text in REVIEW_QUESTIONS:
        question = Question.objects.create(text=question_text)
        questions.append(question)
        print(f"  [OK] Created: {question_text[:50]}...")
    
    return questions


def create_faculty_reviews(faculty_list, students, questions):
    """Create faculty reviews"""
    print("\nCreating faculty reviews...")
    reviews = []
    
    for i in range(NUM_FACULTY_REVIEWS):
        faculty = random.choice(faculty_list)
        student = random.choice(students)
        question = random.choice(questions)
        
        # Determine rating and corresponding review type
        rating = random.randint(0, 10)
        if rating >= 7:
            description = random.choice(POSITIVE_REVIEWS)
            tags = random.sample(['Good', 'Better', 'Best', 'Nice', 'Student Friendly'], k=random.randint(1, 3))
        elif rating >= 4:
            description = random.choice(NEUTRAL_REVIEWS)
            tags = random.sample(['Good', 'Nice'], k=random.randint(0, 2))
        else:
            description = random.choice(NEGATIVE_REVIEWS)
            tags = random.sample(['Worst'], k=random.randint(0, 1))
        
        is_anonymous = random.choice([True, False])
        
        # Create review with a random date in the past year
        review = Review.objects.create(
            faculty=faculty,
            student=student,
            question=question,
            description=description,
            points=rating,
            tags=tags,
            is_anonymous=is_anonymous
        )
        
        # Set random creation date
        days_ago = random.randint(1, 365)
        review.created_at = timezone.now() - timedelta(days=days_ago)
        review.save()
        
        reviews.append(review)
        
        if (i + 1) % 20 == 0:
            print(f"  [OK] Created {i + 1} faculty reviews...")
    
    print(f"  [OK] Total faculty reviews created: {len(reviews)}")
    return reviews


def create_course_reviews(courses, students, questions):
    """Create course reviews"""
    print("\nCreating course reviews...")
    reviews = []
    
    for i in range(NUM_COURSE_REVIEWS):
        course = random.choice(courses)
        student = random.choice(students)
        question = random.choice(questions)
        
        # Determine rating and corresponding review type
        rating = random.randint(0, 10)
        if rating >= 7:
            description = random.choice(COURSE_POSITIVE_REVIEWS)
            tags = random.sample(['Good', 'Better', 'Best', 'Nice', 'Interesting', 'Useful'], k=random.randint(1, 3))
        elif rating >= 4:
            description = random.choice(COURSE_NEUTRAL_REVIEWS)
            tags = random.sample(['Good', 'Nice'], k=random.randint(0, 2))
        else:
            description = random.choice(COURSE_NEGATIVE_REVIEWS)
            tags = random.sample(['Worst', 'Difficult'], k=random.randint(0, 2))
        
        is_anonymous = random.choice([True, False])
        
        # Create review with a random date in the past year
        review = CourseReview.objects.create(
            course=course,
            student=student,
            question=question,
            description=description,
            points=rating,
            tags=tags,
            is_anonymous=is_anonymous
        )
        
        # Set random creation date
        days_ago = random.randint(1, 365)
        review.created_at = timezone.now() - timedelta(days=days_ago)
        review.save()
        
        reviews.append(review)
        
        if (i + 1) % 20 == 0:
            print(f"  [OK] Created {i + 1} course reviews...")
    
    print(f"  [OK] Total course reviews created: {len(reviews)}")
    return reviews


def print_summary():
    """Print summary of created data"""
    print("\n" + "="*60)
    print("DATABASE POPULATION SUMMARY")
    print("="*60)
    print(f"Departments:      {Department.objects.count()}")
    print(f"Courses:          {Course.objects.count()}")
    print(f"Faculty:          {Faculty.objects.count()}")
    print(f"Students:         {Student.objects.count()}")
    print(f"Questions:        {Question.objects.count()}")
    print(f"Faculty Reviews:  {Review.objects.count()}")
    print(f"Course Reviews:   {CourseReview.objects.count()}")
    print("="*60)
    
    # Show some statistics
    print("\nSTATISTICS:")
    print(f"Anonymous Faculty Reviews: {Review.objects.filter(is_anonymous=True).count()}")
    print(f"Anonymous Course Reviews:  {CourseReview.objects.filter(is_anonymous=True).count()}")
    
    # Average ratings
    from django.db.models import Avg
    avg_faculty_rating = Review.objects.aggregate(Avg('points'))['points__avg']
    avg_course_rating = CourseReview.objects.aggregate(Avg('points'))['points__avg']
    
    if avg_faculty_rating:
        print(f"Average Faculty Rating:    {avg_faculty_rating:.2f}/10")
    if avg_course_rating:
        print(f"Average Course Rating:     {avg_course_rating:.2f}/10")
    
    print("="*60)
    print("[OK] Database population completed successfully!")
    print("="*60)


def main():
    """Main function to populate the database"""
    print("="*60)
    print("ClassCritic Database Population Script")
    print("="*60)
    
    if CLEAR_EXISTING_DATA:
        clear_data()
    
    # Create data in order (respecting foreign key dependencies)
    departments = create_departments()
    courses = create_courses(departments)
    faculty_list = create_faculty(departments, courses)
    students = create_students()
    questions = create_questions()
    faculty_reviews = create_faculty_reviews(faculty_list, students, questions)
    course_reviews = create_course_reviews(courses, students, questions)
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
