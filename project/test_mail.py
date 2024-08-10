import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_test_email(to_email):
    subject = 'Test Email Subject'
    message = render_to_string('user/email_templates.html', {
        'user': 'Test User',
        'otp_num': '123456'
    })
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)
    print('Email sent successfully!')

if __name__ == '__main__':
    send_test_email('www.hamidbentafat@gmail.com')  # Replace with the recipient's email
