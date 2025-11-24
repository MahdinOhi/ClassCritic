from django.contrib import admin
from .models import Department, Course, Faculty, Student, Question, Review


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department']
    list_filter = ['department']
    search_fields = ['code', 'name']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'designation', 'department']
    list_filter = ['department', 'designation']
    search_fields = ['name', 'email']
    filter_horizontal = ['courses']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'email_verified']
    list_filter = ['email_verified']
    search_fields = ['name', 'student_id']
    readonly_fields = ['last_otp', 'otp_created_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    search_fields = ['text']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'get_student_name', 'points', 'is_anonymous', 'created_at']
    list_filter = ['is_anonymous', 'points', 'created_at', 'faculty__department']
    search_fields = ['faculty__name', 'student__name', 'description']
    readonly_fields = ['created_at']
    
    def get_student_name(self, obj):
        """Always show actual student name in admin, even for anonymous reviews"""
        if obj.student:
            # Show student name with (Anonymous) indicator if review is anonymous
            if obj.is_anonymous:
                return f'{obj.student.name} (Anonymous)'
            return obj.student.name
        return 'Unknown'
    get_student_name.short_description = 'Student (Actual Name)'
    
    def has_add_permission(self, request):
        # Reviews should be added through the frontend
        return False
    
    def has_change_permission(self, request, obj=None):
        # Reviews should not be edited
        return False
