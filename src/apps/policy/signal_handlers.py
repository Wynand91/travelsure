from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from apps.policy.models import Policy
from apps.policy.utils import calculate_price
from apps.utils.utils import send_email


@receiver(post_save, sender=Policy)
def send_payment_details(instance: Policy, created, **_):
    if not created:
        return

    subject = 'Your Policy Confirmation'
    recipient = instance.user.username
    context = {'policy': instance, 'price': calculate_price(instance)}
    html_content = render_to_string('emails/policy/policy_confirmation.html', context)
    send_email(subject, html_content, recipient)
