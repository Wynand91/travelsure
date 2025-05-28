from datetime import datetime
from django.core import mail


from rest_framework.reverse import reverse_lazy

from apps.policy.enums import PolicyStatus
from apps.policy.models import Policy
from tests.base import BaseApiTestCase
from tests.factories import UserFactory, PolicyFactory

from pytest_voluptuous import S


class TestClaimsApi(BaseApiTestCase):
    url = reverse_lazy('api:claims-list')

    def setUp(self):
        self.user = UserFactory()
        self.policy_expired_old = PolicyFactory(user=self.user, status=PolicyStatus.EXPIRED)
        self.policy_expired_recent = PolicyFactory(user=self.user, status=PolicyStatus.EXPIRED)
        self.policy_pending = PolicyFactory(status=PolicyStatus.PENDING)
        self.policy_cancelled = PolicyFactory(status=PolicyStatus.CANCELLED)
        self.policy_active = PolicyFactory(user=self.user)

        # clear any mails created by factories
        mail.outbox.clear()

    def test_claim_list(self):
        resp = self.get(user=self.user)
        assert resp.status_code == 200
        json = resp.json()
        breakpoint()
        # check that both policies belong to request user
        assert len(json) == 2
        for policy in json:
            assert policy['user'] == str(self.user.id)
        # check response list structure
        assert json == S([
            {
                'id': str,
                'destination': str,
                'start_date': str,
                'end_date': str,
                'policy_type': str,
                'status': str,
                'is_active': bool,
                'paid': True,
                'user': str
            }
        ])


    def test_claim_detail(self):
        url = reverse_lazy('api:policy-detail', kwargs={'pk': self.policy_active.id})
        resp = self.get(user=self.user, url=url)
        assert resp.status_code == 200
        breakpoint()
        assert resp.json() == {
            'id': str(self.policy_active.id),
            'destination': 'EUROPE',
            'start_date': '2025-10-30',
            'end_date': '2025-12-30',
            'policy_type': 'PREMIUM',
            'status': 'ACTIVE',
            'is_active': True,
            'paid': True,
            'user': str(self.user.id)
        }

    def test_claim_create_validation(self):
        resp = self.post(user=self.user, data={})
        assert resp.status_code == 400
        breakpoint()
        assert resp.json() == {
            'policy': str(self.policy_active.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_for_pending_policy(self):
        data = {
            'policy': str(self.policy_pending.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        breakpoint()
        assert resp.json() == {
            'destination': ['Not a valid enum.'],
            'policy_type': ['Not a valid enum.']
        }
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_for_cancelled_policy(self):
        data = {
            'policy': str(self.policy_pending.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        breakpoint()
        assert resp.json() == {
            'destination': ['Not a valid enum.'],
            'policy_type': ['Not a valid enum.']
        }
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_for_long_expired_policy(self):
        data = {
            'policy': str(self.policy_expired_old.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        breakpoint()
        assert resp.json() == {
            'destination': ['Not a valid enum.'],
            'policy_type': ['Not a valid enum.']
        }
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_invalid_date(self):
        data = {
            'destination': 'EUROPE',
            'start_date': '2026-06-30',
            'end_date': '2020-07-30',
            'policy_type': 'BASIC',
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'non_field_errors': ['Start date can not be after End date']}
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_success_expired_policy(self):
        data = {
            'destination': 'EUROPE',
            'start_date': '2025-06-30',
            'end_date': '2025-07-30',
            'policy_type': 'BASIC',
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 201
        obj = Policy.objects.get(id=resp.json()['id'])
        assert resp.json() == {
            'id': str(obj.id),
            'destination': 'EUROPE',
            'start_date': '2025-06-30',
            'end_date': '2025-07-30',
            'policy_type': 'BASIC',
            'status': 'PENDING',
            'is_active': False,
            'paid': False,
            'user': str(self.user.id)
        }
        # check email was sent
        # Check how many emails were sent
        assert len(mail.outbox) == 1

        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == "Your Policy Confirmation"
        assert "Thank you" in email.body
        assert email.to == [self.user.username]


    def test_claim_create_success_active_policy(self):
        data = {
            'destination': 'EUROPE',
            'start_date': '2025-06-30',
            'end_date': '2025-07-30',
            'policy_type': 'BASIC',
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 201
        obj = Policy.objects.get(id=resp.json()['id'])
        assert resp.json() == {
            'id': str(obj.id),
            'destination': 'EUROPE',
            'start_date': '2025-06-30',
            'end_date': '2025-07-30',
            'policy_type': 'BASIC',
            'status': 'PENDING',
            'is_active': False,
            'paid': False,
            'user': str(self.user.id)
        }
        # check email was sent
        # Check how many emails were sent
        assert len(mail.outbox) == 1

        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == "Your Policy Confirmation"
        assert "Thank you" in email.body
        assert email.to == [self.user.username]

