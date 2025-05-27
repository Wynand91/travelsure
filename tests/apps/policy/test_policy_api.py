from datetime import datetime

from rest_framework.reverse import reverse_lazy

from apps.policy.enums import PolicyStatus
from apps.policy.models import Policy
from tests.base import BaseApiTestCase
from tests.factories import UserFactory, PolicyFactory

from pytest_voluptuous import S


class TestPolicyCreateApi(BaseApiTestCase):
    url = reverse_lazy('api:policy-list')

    def setUp(self):
        self.user = UserFactory()
        self.policy_inactive = PolicyFactory(user=self.user, status=PolicyStatus.EXPIRED)
        self.policy_active = PolicyFactory(
            user=self.user,
            start_date=datetime(2025, 10, 30),
            end_date=datetime(2025, 12, 30),
        )

        # create policy for another user
        self.other_user = UserFactory(username='random@user.com')
        self.other_user_policy = PolicyFactory(user=self.other_user)

    def test_policy_list(self):
        resp = self.get(user=self.user)
        assert resp.status_code == 200
        json = resp.json()
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


    def test_policy_detail(self):
        url = reverse_lazy('api:policy-detail', kwargs={'pk': self.policy_active.id})
        resp = self.get(user=self.user, url=url)
        assert resp.status_code == 200
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


    def test_policy_create_validation(self):
        resp = self.post(user=self.user, data={})
        assert resp.status_code == 400
        assert resp.json() == {
            'destination': ['This field is required.'],
            'start_date': ['This field is required.'],
            'end_date': ['This field is required.'],
            'policy_type': ['This field is required.'],
        }

    def test_policy_create_invalid_enum(self):
        data = {
            'destination': 'INVALID',
            'start_date': '2025-06-30',
            'end_date': '2025-07-30',
            'policy_type': 'INVALID',
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {
            'destination': ['Not a valid enum.'],
            'policy_type': ['Not a valid enum.']
        }

    def test_policy_create_invalid_date(self):
        data = {
            'destination': 'EUROPE',
            'start_date': '2026-06-30',
            'end_date': '2020-07-30',
            'policy_type': 'BASIC',
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'non_field_errors': ['Start date can not be after End date']}

    def test_policy_create_success(self):
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
