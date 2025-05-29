from django.core import mail
from freezegun import freeze_time
from rest_framework.reverse import reverse_lazy

from apps.claims.enums import ClaimStatus
from apps.claims.models import Claim
from apps.policy.enums import PolicyStatus
from tests.base import BaseApiTestCase
from tests.factories import UserFactory, PolicyFactory, ClaimFactory


class TestClaimsApi(BaseApiTestCase):
    url = reverse_lazy('api:claim-list')

    def setUp(self):
        # user for create and validation tests (can't have existing claims)
        self.user = UserFactory(username='user1@test.com')
        self.policy_expired_old = PolicyFactory(user=self.user, status=PolicyStatus.EXPIRED)
        self.policy_expired_recent = PolicyFactory(user=self.user, status=PolicyStatus.EXPIRED)
        self.policy_pending = PolicyFactory(status=PolicyStatus.PENDING)
        self.policy_cancelled = PolicyFactory(status=PolicyStatus.CANCELLED)
        self.policy_active = PolicyFactory(user=self.user)

        # add another user to test list/detail view
        self.user2 = UserFactory(username='user2@test.com')
        self.user2_policy = PolicyFactory(user=self.user2)
        self.user2_claim = ClaimFactory(policy=self.user2_policy)

        # clear any mails created by factories
        mail.outbox.clear()

    def test_claim_list(self):
        resp = self.get(user=self.user2)
        assert resp.status_code == 200
        json = resp.json()
        assert len(json) == 1
        assert json[0]['policy_detail']['user'] == str(self.user2.id)
        # check response list structure
        assert json == [
            {
                'id': str(self.user2_claim.id),
                'policy_detail': {
                    'id': str(self.user2_policy.id),
                    'destination': 'EUROPE',
                    'start_date': '2025-05-27',
                    'end_date': '2025-08-27',
                    'policy_type': 'PREMIUM',
                    'status': 'ACTIVE',
                    'is_active': True,
                    'paid': True,
                    'user': str(self.user2.id)
                },
                'description': 'I have a headache and need ibuprofen.',
                'claim_date': '2025-05-30',
                'amount_claimed': '20.00',
                'status': 'PENDING'
            }
        ]


    def test_claim_detail(self):
        url = reverse_lazy('api:claim-detail', kwargs={'pk': self.user2_claim.id})
        resp = self.get(user=self.user2, url=url)
        assert resp.status_code == 200
        assert resp.json() == {
            'id': str(self.user2_claim.id),
            'policy_detail': {
                'id': str(self.user2_policy.id),
                'destination': 'EUROPE',
                'start_date': '2025-05-27',
                'end_date': '2025-08-27',
                'policy_type': 'PREMIUM',
                'status': 'ACTIVE',
                'is_active': True,
                'paid': True,
                'user': str(self.user2.id)
            },
            'description': 'I have a headache and need ibuprofen.',
            'claim_date': '2025-05-30',
            'amount_claimed': '20.00',
            'status': 'PENDING'
        }

    def test_claim_create_validation(self):
        resp = self.post(user=self.user, data={})
        assert resp.status_code == 400
        assert resp.json() == {
            'policy': ['This field is required.'],
            'description': ['This field is required.'],
            'amount_claimed': ['This field is required.']
        }
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_existing_pending_claim(self):
        """
        If there is an existing claim on a policy that is in a pending state, a new claim can
        not be created for that policy.
        """
        ClaimFactory(policy=self.policy_active)
        data = {
            'policy': str(self.policy_active.id),
            'description': 'Broke my other toe now.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'non_field_errors': ['Current pending claim already exists for this policy.']}

    def test_claim_create_existing_rejected_claim(self):
        """
        If there is a existing claim for the policy, but the claim has been rejected, the user
        should be able to create a new claim.
        """
        ClaimFactory(policy=self.policy_active, status=ClaimStatus.REJECTED)
        mail.outbox.clear()
        data = {
            'policy': str(self.policy_active.id),
            'description': 'Broke my other toe now.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 201
        new_claim = Claim.objects.get(id=resp.json()['id'])

        # check email was sent
        assert len(mail.outbox) == 1
        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == 'Claim Confirmation'
        assert str(new_claim.policy.id) in email.body
        assert email.to == [self.user.username]

    def test_claim_create_for_pending_policy(self):
        data = {
            'policy': str(self.policy_pending.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'non_field_errors': ['Invalid policy status']}
        # assert no email sent
        assert len(mail.outbox) == 0

    def test_claim_create_for_cancelled_policy(self):
        data = {
            'policy': str(self.policy_cancelled.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 200,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'non_field_errors': ['Invalid policy status']}
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
        assert resp.json() == {'non_field_errors': ['Claim window expired']}
        # assert no email sent
        assert len(mail.outbox) == 0

    @freeze_time('2025-05-29')
    def test_claim_create_success_active_policy(self):
        """
        User can claim from active policy.
        """
        data = {
            'policy': str(self.policy_active.id),
            'description': 'Broke my toe. Ouchie.',
            'amount_claimed': 50,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 201
        resp_json = resp.json()
        new_claim = Claim.objects.get(id=resp_json['id'])
        assert resp_json == {
            'id': str(new_claim.id),
            'policy_detail': {
                'id': str(new_claim.policy.id),
                'destination': 'EUROPE',
                'start_date': '2025-05-27',
                'end_date': '2025-08-27',
                'policy_type': 'PREMIUM',
                'status': 'ACTIVE',
                'is_active': True,
                'paid': True,
                'user': str(self.user.id)
            },
            'description': 'Broke my toe. Ouchie.',
            'claim_date': '2025-05-29',
            'amount_claimed': '50.00',
            'status': 'PENDING'
        }

        # check email was sent
        assert len(mail.outbox) == 1
        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == 'Claim Confirmation'
        assert str(new_claim.policy.id) in email.body
        assert email.to == [self.user.username]

    @freeze_time('2025-09-26')  # just within 30 grace period
    def test_claim_create_success_expired_policy(self):
        """
        If policy has expired less than 30 days ago, user can still claim.
        """
        data = {
            'policy': str(self.policy_expired_recent.id),
            'description': 'Broke my toenail.',
            'amount_claimed': 1000,
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 201
        resp_json = resp.json()
        new_claim = Claim.objects.get(id=resp_json['id'])
        assert resp_json == {
            'id': str(new_claim.id),
            'policy_detail': {
                'id': str(new_claim.policy.id),
                'destination': 'EUROPE',
                'start_date': '2025-05-27',
                'end_date': '2025-08-27',
                'policy_type': 'PREMIUM',
                'status': 'EXPIRED',
                'is_active': True,
                'paid': True,
                'user': str(self.user.id)
            },
            'description': 'Broke my toenail.',
            'claim_date': '2025-09-26',
            'amount_claimed': '1000.00',
            'status': 'PENDING'
        }

        # check email was sent
        assert len(mail.outbox) == 1
        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == 'Claim Confirmation'
        assert str(new_claim.policy.id) in email.body
        assert email.to == [self.user.username]


    def test_claim_status_action(self):
        url = reverse_lazy('api:claim-status', kwargs={'pk': self.user2_claim.id})
        resp = self.get(user=self.user2, url=url)
        assert resp.status_code == 200
        assert resp.json() == {
            'policy_id': str(self.user2_claim.policy.id),
            'status': 'PENDING'
        }

        # test that another user can't access the object
        resp = self.get(user=self.user, url=url)
        assert resp.status_code == 404
