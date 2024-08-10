# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=UserProfile)
def send_otp_email(sender, instance, created, **kwargs):
    if created:
        # Retrieve OTP from session (this will be passed through the view)
        otp_num = instance.otp_code  
        user_id = instance.id
        user=User.objects.get(id=user_id)
        print(otp_num)
        print(user)
        # Prepare the email
        subject = 'Your OTP code'
        message = render_to_string('user/email_templates.html', {
            'user': user.username,
            'otp_num': otp_num
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)
