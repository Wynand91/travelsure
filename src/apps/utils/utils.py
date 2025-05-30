from django.core.mail import EmailMessage
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


def send_email(subject, html_content, receiver):
    email = EmailMessage(subject, html_content, to=[receiver])
    email.content_subtype = 'html'
    email.send()


def check_expiry_date(date_to_check, days_allowed):
    difference = now().date() - date_to_check
    if abs(difference.days) > days_allowed:
        raise ValidationError('Claim window expired')
