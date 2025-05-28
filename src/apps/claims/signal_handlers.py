from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from apps.policy.models import Claim
from apps.policy.utils import calculate_price
from apps.utils.utils import send_email


@receiver(post_save, sender=Claim)
def send_claim_confirmation(instance: Claim, created, **_):
    if not created:
        return

    subject = 'Your Policy Confirmation'
    recipient = instance.user.username
    context = {'policy': instance, 'price': calculate_price(instance)}
    html_content = render_to_string('emails/policy/policy_confirmation.html', context)
    send_email(subject, html_content, recipient)


@receiver(post_save, sender=Claim)
def send_claim_status_apdate(instance: Claim, created, **_):
    if not created:
        return

    subject = 'Your Policy Confirmation'
    recipient = instance.user.username
    context = {'policy': instance, 'price': calculate_price(instance)}
    html_content = render_to_string('emails/policy/policy_confirmation.html', context)
    send_email(subject, html_content, recipient)