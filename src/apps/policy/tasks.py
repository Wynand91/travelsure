from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from apps.policy.models import Policy, PolicyStatus


@db_periodic_task(crontab(hour=0, minute=1))  # 00:01
def deactivate_policies():
    """
    Deactivate all policies that are active, if they had an end_date of yesterday
    """
    yesterday = timezone.now() - timedelta(days=1)
    Policy.objects.filter(
        status=PolicyStatus.ACTIVE,
        end_date=yesterday.date()
    ).update(status=PolicyStatus.EXPIRED)


@db_periodic_task(crontab(hour=0, minute=5))  # 00:05
def activate_policies():
    """
    Activate all policies that are still in a pending state, that have been paid, and with a
    start_date of today.
    """
    today = timezone.now().date()
    Policy.objects.filter(
        status=PolicyStatus.PENDING,
        paid=True,
        start_date=today
    ).update(status=PolicyStatus.ACTIVE)
