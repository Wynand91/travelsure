from datetime import timezone

from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError


def send_email(subject, html_content, receiver):
    email = EmailMessage(subject, html_content, to=[receiver])
    email.content_subtype = 'html'
    email.send()


def check_expiry_date(date_to_check,  months_allowed):
    breakpoint()
    raise ValidationError('Claim window expired')