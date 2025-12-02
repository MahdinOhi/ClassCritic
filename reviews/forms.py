from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Review, CourseReview, validate_student_email


class StudentRegistrationForm(forms.Form):
    """Form for student registration with email validation"""
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.EmailField(
        validators=[validate_student_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.name@std.ewubd.edu'
        }),
        help_text='Must be a valid @std.ewubd.edu email address'
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@std.ewubd.edu'):
            raise ValidationError('Only @std.ewubd.edu email addresses are allowed.')
        return email


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter 6-digit OTP',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        })
    )


class ReviewForm(forms.ModelForm):
    """Form for submitting reviews"""
    
    class Meta:
        model = Review
        fields = ['faculty', 'question', 'description', 'points', 'tags', 'is_anonymous']
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'question': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your review about the faculty',
                'rows': 6,
                'id': 'review-description'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0',
                'max': '10',
                'type': 'range',
                'id': 'points-slider'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].required = False
        self.fields['tags'].required = False
        
        # Convert tags to choices for checkbox
        tag_choices = [(tag[0], tag[0]) for tag in Review.TAG_CHOICES]
        self.fields['tags'] = forms.MultipleChoiceField(
            choices=tag_choices,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-group'}),
            required=False
        )
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        # No minimum word count requirement
        return description
    
    def clean_points(self):
        points = self.cleaned_data.get('points')
        if points is not None and (points < 0 or points > 10):
            raise ValidationError('Points must be between 0 and 10.')
        return points


class CourseReviewForm(forms.ModelForm):
    """Form for submitting course reviews"""
    
    class Meta:
        model = CourseReview
        fields = ['course', 'question', 'description', 'points', 'tags', 'is_anonymous']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'question': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your review about the course',
                'rows': 6,
                'id': 'course-review-description'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0',
                'max': '10',
                'type': 'range',
                'id': 'course-points-slider'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].required = False
        self.fields['tags'].required = False
        
        # Convert tags to choices for checkbox
        tag_choices = [(tag[0], tag[0]) for tag in CourseReview.TAG_CHOICES]
        self.fields['tags'] = forms.MultipleChoiceField(
            choices=tag_choices,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-group'}),
            required=False
        )
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        # No minimum word count requirement
        return description
    
    def clean_points(self):
        points = self.cleaned_data.get('points')
        if points is not None and (points < 0 or points > 10):
            raise ValidationError('Points must be between 0 and 10.')
        return points
