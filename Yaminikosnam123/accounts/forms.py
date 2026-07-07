from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from mentorapp.departments import DEPARTMENT_CHOICES
import re


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username or email is required.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('Password is required.')
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters.')
        return password


class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'required': 'required',
            'pattern': '[a-zA-Z\\s\\.\\-]+'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': 'required'
        })
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'pattern': '[0-9\\-\\+\\s\\(\\)]+'
        })
    )

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'required': 'required',
            'minlength': '8'
        })
    )

    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'required': 'required',
            'minlength': '8'
        })
    )

    terms_accepted = forms.BooleanField(
        required=False,
        error_messages={
            'required': 'You must accept the terms and conditions.'
        },
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Full name is required.')
        if not re.match(r'^[a-zA-Z\s\.\-]+$', name):
            raise ValidationError('Name should contain only letters, spaces, dots, or hyphens.')
        if len(name.strip()) < 2:
            raise ValidationError('Name must be at least 2 characters.')
        return name.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[0-9\-\+\s\(\)]+$', phone):
            raise ValidationError('Invalid phone number format.')
        return phone

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if not department or department == '':
            raise ValidationError('Please select a department.')
        return department

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError('Password is required.')
        
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        # Check for digit
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        
        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            raise ValidationError('Password must contain at least one special character (!@#$%^&*).')
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        name = cleaned_data.get('name')

        # Check if passwords match
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match.')

        # Check if username already exists
        if name:
            if User.objects.filter(username=name).exists():
                raise ValidationError('This username is already taken. Please choose a different name.')

        return cleaned_data
