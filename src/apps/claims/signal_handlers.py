from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from apps.claims.enums import ClaimStatus
from apps.claims.models import Claim
from apps.claims.utils import get_template_for_status
from apps.utils.utils import send_email


@receiver(post_save, sender=Claim)
def send_claim_confirmation(instance: Claim, created, **_):
    if not created:
        return

    subject = 'Claim Confirmation'
    recipient = instance.policy.user.username
    context = {'plan': instance.policy.id}
    html_content = render_to_string('emails/claims/claim_confirmation.html', context)
    send_email(subject, html_content, recipient)


@receiver(pre_save, sender=Claim)
def send_claim_status_update(sender: Claim, instance: Claim, **_):
    """
    Once an admin updates the status of Claim, an email should be fired.
    """
    try:
        old_instance = Claim.objects.get(id=instance.id)
    except Claim.DoesNotExist:
        # if it's a new object, we can skip.
        return

    # check if status field was updated
    if old_instance.status != instance.status and instance.status != ClaimStatus.PENDING:
        subject = 'Claim Result'
        recipient = instance.policy.user.username
        context = {'plan': instance.policy.id}
        template = get_template_for_status(instance.status)
        html_content = render_to_string(f'emails/claims/{template}', context)
        send_email(subject, html_content, recipient)