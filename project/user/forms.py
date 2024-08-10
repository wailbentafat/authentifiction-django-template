from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import random
import requests
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    email = forms.EmailField(label='Email Address', help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        
    def clean_password2(self):
        """
        Validate that the two password fields match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        return password2

    def clean_username(self):
        """
        Validate that the username does not already exist in the database.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username

    def clean_email(self):
        """
        Validate that the email does not already exist in the database and is valid.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')

        # Additional email validation
        api_key = '5f2b341945492ab36601fad393d509054d668604'  # Replace with your Hunter.io API key
        url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}'
        response = requests.get(url)
        result = response.json()
        print(result)
        verification_status = result.get('data', {}).get('status', 'unknown')
        if verification_status != 'valid':
            raise ValidationError('Invalid email address.')
        
        return email
class otp(forms.Form):
    code = forms.CharField(label='Enter OTP')
    
    
    