from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('faculty/<int:faculty_id>/', views.faculty_detail, name='faculty_detail'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('search/', views.search_reviews, name='search_reviews'),
    path('logout/', views.logout_view, name='logout'),
    # Course-related URLs
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('submit-course-review/', views.submit_course_review, name='submit_course_review'),
]
