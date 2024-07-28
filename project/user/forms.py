from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import random
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    email = forms.EmailField(label='Email Address', help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
    def check_passwords(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
    def user_exists(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
       
    def email_exists(self):
        email=self.cleaned_data.get('email')
        number=random.randint(1000,9999)
        self.code=number
        my='wailbentafat@gmail.com'
        subject=_('verification code')
        message=_(f'your verification code is {number}')
        send_mail(subject,message,my,[email])
        return self.code