from apps.users.models import User
from rest_framework.reverse import reverse_lazy

from tests.base import BaseApiTestCase


class TestUserCreate(BaseApiTestCase):
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
        assert User.objects.get(id=resp.json()['id'])

