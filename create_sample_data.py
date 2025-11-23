from reviews.models import Department, Course, Faculty, Question

# Create Departments
cs_dept = Department.objects.create(name="Computer Science & Engineering")
math_dept = Department.objects.create(name="Mathematics & Natural Sciences")
eng_dept = Department.objects.create(name="English & Humanities")

# Create Courses
course1 = Course.objects.create(name="Data Structures", code="CSE207", department=cs_dept)
course2 = Course.objects.create(name="Algorithms", code="CSE225", department=cs_dept)
course3 = Course.objects.create(name="Database Systems", code="CSE303", department=cs_dept)
course4 = Course.objects.create(name="Calculus I", code="MATH101", department=math_dept)
course5 = Course.objects.create(name="English Composition", code="ENG101", department=eng_dept)

# Create Faculty
faculty1 = Faculty.objects.create(
    name="Dr. Sarah Ahmed",
    email="sarah.ahmed@ewubd.edu",
    designation="Associate Professor",
    department=cs_dept
)
faculty1.courses.add(course1, course2)

faculty2 = Faculty.objects.create(
    name="Dr. Mohammad Rahman",
    email="mohammad.rahman@ewubd.edu",
    designation="Professor",
    department=cs_dept
)
faculty2.courses.add(course2, course3)

faculty3 = Faculty.objects.create(
    name="Dr. Fatima Khan",
    email="fatima.khan@ewubd.edu",
    designation="Assistant Professor",
    department=math_dept
)
faculty3.courses.add(course4)

faculty4 = Faculty.objects.create(
    name="Dr. John Smith",
    email="john.smith@ewubd.edu",
    designation="Senior Lecturer",
    department=eng_dept
)
faculty4.courses.add(course5)

# Create Questions
Question.objects.create(text="How would you rate the teaching quality?")
Question.objects.create(text="How helpful was the faculty outside of class?")
Question.objects.create(text="How fair was the grading system?")
Question.objects.create(text="Would you recommend this faculty to other students?")

print("Sample data created successfully!")
print(f"Departments: {Department.objects.count()}")
print(f"Courses: {Course.objects.count()}")
print(f"Faculty: {Faculty.objects.count()}")
print(f"Questions: {Question.objects.count()}")
