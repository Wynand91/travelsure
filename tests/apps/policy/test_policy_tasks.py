from datetime import datetime, timedelta

from apps.policy.enums import PolicyStatus
from apps.policy.models import Policy
from apps.policy.tasks import deactivate_policies, activate_policies
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from tests.factories import UserFactory, PolicyFactory


class PolicyTaskTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        # these policies SHOULD NOT get updated
        # not paid
        self.unpaid = PolicyFactory(
            paid=False,
            status=PolicyStatus.PENDING,
            start_date=datetime(2025, 10, 30),
            end_date=datetime(2025, 12, 30)
        )
        # cancelled
        self.cancelled = PolicyFactory(
            paid=True,
            status=PolicyStatus.CANCELLED,
            start_date=datetime(2025, 10, 30),
            end_date=datetime(2025, 12, 30)
        )
        # paid and pending, but not start_date yet
        self.not_started = PolicyFactory(
            paid=True,
            status=PolicyStatus.PENDING,
            start_date=datetime(2025, 10, 31),
            end_date=datetime(2025, 12, 30)
        )

        # these 2 policies SHOULD get activated by the tasks (paid and pending and start_date)
        PolicyFactory.create_batch(
            2,
            status=PolicyStatus.PENDING,
            paid=True,
            start_date=datetime(2025, 10, 30),
            end_date=datetime(2025, 12, 30)
        )

        # these 2 policies SHOULD get deactivated (paid, active policies) after end_date
        PolicyFactory.create_batch(
            2,
            start_date=datetime(2025, 9, 30),
            end_date=datetime(2025, 10, 29)
        )

    @freeze_time('2025-10-30 00:00:01')
    def test_deactivate_policy_task(self):
        yesterday = timezone.now() - timedelta(days=1)
        expired_policies = Policy.objects.filter(
            status=PolicyStatus.EXPIRED,
            end_date=yesterday.date()
        )
        assert expired_policies.count() == 0
        # there should be 2 EXPIRED policies after task runs
        deactivate_policies()
        assert expired_policies.count() == 2

    @freeze_time('2025-10-30 00:00:05')
    def test_activate_policy_task(self):
        active_policies = Policy.objects.filter(
            status=PolicyStatus.ACTIVE,
            start_date=timezone.now().date()
        )
        assert active_policies.count() == 0
        # there should be 2 ACTIVE policies after task runs
        activate_policies()
        assert active_policies.count() == 2
