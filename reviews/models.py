from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_student_email(value):
    """Validate that email ends with @std.ewubd.edu"""
    if not value.endswith('@std.ewubd.edu'):
        raise ValidationError(
            'Only @std.ewubd.edu email addresses are allowed for student registration.'
        )


# Word count validation removed - no minimum word requirement


class Department(models.Model):
    """Department model - represents academic departments"""
    name = models.CharField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model - represents courses offered by departments"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        related_name='courses'
    )
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Faculty(models.Model):
    """Faculty model - represents faculty members"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='faculty_members'
    )
    courses = models.ManyToManyField(Course, related_name='faculty_members', blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Faculty'
    
    def __str__(self):
        return self.name
    
    def average_rating(self):
        """Calculate average rating from all reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.points for r in reviews) / reviews.count(), 2)
        return 0
    
    def total_reviews(self):
        """Get total number of reviews"""
        return self.reviews.count()


class Student(models.Model):
    """Student model - represents students who can submit reviews"""
    name = models.CharField(max_length=200)
    student_id = models.EmailField(
        unique=True,
        validators=[validate_student_email],
        help_text='Must be a valid @std.ewubd.edu email address'
    )
    email_verified = models.BooleanField(default=False)
    last_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
    def is_otp_valid(self):
        """Check if OTP is still valid (within 5 minutes)"""
        if not self.otp_created_at:
            return False
        expiry_time = self.otp_created_at + timedelta(minutes=5)
        return timezone.now() < expiry_time


class Question(models.Model):
    """Question model - represents review questions"""
    text = models.TextField()
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')


class Review(models.Model):
    """Review model - represents student reviews of faculty"""
    
    TAG_CHOICES = [
        ('Good', 'Good'),
        ('Better', 'Better'),
        ('Best', 'Best'),
        ('Worst', 'Worst'),
        ('Nice', 'Nice'),
        ('Student Friendly', 'Student Friendly'),
    ]
    
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        help_text='Student who submitted the review (stored even for anonymous reviews)'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews'
    )
    description = models.TextField(
        help_text='Write your review about the faculty'
    )
    points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Rating from 0 to 10'
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text='Select from predefined tags'
    )
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        # Display as anonymous on public site, but student is always stored for admin
        if self.is_anonymous:
            student_name = 'Anonymous'
        else:
            student_name = self.student.name if self.student else 'Unknown'
        return f"Review by {student_name} for {self.faculty.name}"
    
    def clean(self):
        """Validate tags are from allowed choices"""
        if self.tags:
            allowed_tags = [tag[0] for tag in self.TAG_CHOICES]
            for tag in self.tags:
                if tag not in allowed_tags:
                    raise ValidationError(f"Invalid tag: {tag}. Allowed tags: {', '.join(allowed_tags)}")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
