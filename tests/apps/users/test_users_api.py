from apps.users.models import User
from pytest_voluptuous import S
from rest_framework.reverse import reverse_lazy

from tests.base import BaseApiTestCase
from tests.factories import UserFactory, PASSWORD


class TestUserCreateApi(BaseApiTestCase):
    url = reverse_lazy('api:user-list')

    def test_user_create_no_email(self):
        resp = self.post(data={})
        assert resp.status_code == 400
        assert resp.json() == {
            'username': ['This field is required.'],
            'password': ['This field is required.']
        }

    def test_user_create_validate_password(self):
        data = {
            'username': 'john@test.com',
            'password': '1234'
        }
        resp = self.post(data=data)
        assert resp.status_code == 400
        assert resp.json() == {
            'password': [
                'This password is too short. It must contain at least 8 characters.',
                'This password is too common.',
                'This password is entirely numeric.'
            ]
        }

    def test_user_create_validate_username(self):
        data = {
            'username': 'john',
            'password': 'LolC@t123'
        }
        resp = self.post(data=data)
        assert resp.status_code == 400
        assert resp.json() == {'username': ['Enter a valid email address.']}

    def test_user_create_success(self):
        data = {
            'username': 'john@test.com',
            'first_name': 'john',
            'last_name': 'test',
            'password': 'Lolc@t124'
        }
        resp = self.post(data=data)
        assert resp.status_code == 201
        new_user = User.objects.get(id=resp.json()['id'])
        assert resp.json() == S({
            'id': str(new_user.id),
            'username': 'john@test.com',
            'auth_token': str,
            'refresh_token': str,
        })


class TestUserProfileApi(BaseApiTestCase):
    url = reverse_lazy('api:user-profile')

    def setUp(self):
        self.user = UserFactory()

    def test_profile_auth(self):
        resp = self.client.get(self.url)
        assert resp.status_code == 401
        assert resp.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_profile_get(self):
        resp = self.get(user=self.user)
        assert resp.status_code == 200
        assert resp.json() == {
            'id': str(self.user.id),
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        }


class TestUserChangePasswordApi(BaseApiTestCase):
    url = reverse_lazy('api:user-change-password')

    def setUp(self):
        self.user = UserFactory()

    def test_change_password_validation(self):
        data = {}
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {
            'old_password': ['This field is required.'],
            'new_password': ['This field is required.'],
            'new_password_confirm': ['This field is required.']
        }

    def test_change_password_incorrect(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'Th1sIsNewp@ss',
            'new_password_confirm': 'Th1sIsNewp@ss'
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'old_password': ['Old password is incorrect.']}

    def test_change_password_confirm_incorrect(self):
        data = {
            'old_password': PASSWORD,
            'new_password': 'Th1sIsNewp@ss',
            'new_password_confirm': 'nomatch'
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'new_password_confirm': ['Confirm password does not match new password.']}

    def test_change_password_new_pass_validation(self):
        invalid_password = 'invalid'
        data = {
            'old_password': PASSWORD,
            'new_password': invalid_password,
            'new_password_confirm': invalid_password
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 400
        assert resp.json() == {'new_password': ['This password is too short. It must contain at least 8 characters.']}

    def test_change_password_success(self):
        valid_password = 'NewP@ssword'
        data = {
            'old_password': PASSWORD,
            'new_password': valid_password,
            'new_password_confirm': valid_password
        }
        resp = self.post(user=self.user, data=data)
        assert resp.status_code == 204  # No content
        # check that password was updated
        self.user.refresh_from_db()
        assert self.user.check_password(valid_password)
