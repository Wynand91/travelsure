from django.contrib.admin import AdminSite
from django.http import HttpRequest
from django.test import TestCase

from apps.policy.admin import PolicyAdmin
from apps.policy.models import Policy
from tests.factories import UserFactory


def get_mock_request(user):
    request = HttpRequest()
    request.GET = {}  # Required for get_actions
    request.user = user
    return request


class TestReadOnlyAdmin(TestCase):

    def setUp(self):
        self.super_user = UserFactory(is_staff=True, is_superuser=True, username='super@user.com')
        self.normal_user = UserFactory(is_staff=True, is_superuser=False, username='admin@user.com')
        self.admin = PolicyAdmin(Policy, AdminSite())  # uses ReadOnlyAdmin
        self.normal_req = get_mock_request(self.normal_user)
        self.super_req = get_mock_request(self.super_user)

    def test_has_add_permission(self):
        # normal admin
        assert not self.admin.has_add_permission(self.normal_req)
        # superuser
        assert self.admin.has_add_permission(self.super_req)

    def test_change_permission(self):
        # normal admin
        assert not self.admin.has_change_permission(self.normal_req)
        # superuser
        assert self.admin.has_change_permission(self.super_req)

    def test_delete_permission(self):
        # normal admin
        assert not self.admin.has_delete_permission(self.normal_req)
        # superuser
        assert self.admin.has_delete_permission(self.super_req)

    def test_readonly_fields(self):
        # normal admin
        readonly_fields = self.admin.get_readonly_fields(self.normal_req)
        # all fields should be readonly for normal admins
        expected_fields = [f.name for f in Policy._meta.fields]
        assert sorted(readonly_fields) == sorted(expected_fields)

        # superuser
        self.admin.readonly_fields = ['status']
        readonly_fields = self.admin.get_readonly_fields(self.super_req)
        # only the readonly fields should be readonly for superusers
        assert readonly_fields == ['status']

    def test_get_actions(self):
        # Add a fake action for testing
        def dummy_action():
            pass
        self.admin.actions = [dummy_action]

        # normal admin
        actions = self.admin.get_actions(self.normal_req)
        assert isinstance(actions, dict)
        assert 'dummy_action' not in actions

        # superuser
        actions = self.admin.get_actions(self.super_req)
        assert isinstance(actions, dict)
        assert 'dummy_action' in actions
