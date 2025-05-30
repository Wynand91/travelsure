from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from tests.utils import get_jwt_token


class BaseApiTestCase(APITestCase):
    """
    Base API test case class for cleaner and more readable/explicit requests definitions in unit tests.
    """
    client: APIClient

    @property
    def url(self):
        raise NotImplementedError

    def request(
        self,
        method='post',
        data=None, url=None,
        user=None, jwt=None,
        **kwargs
    ) -> Response:
        if user:
            kwargs['HTTP_AUTHORIZATION'] = f'Bearer {get_jwt_token(user)}'
        elif jwt:
            kwargs['HTTP_AUTHORIZATION'] = f'Bearer {jwt}'
        return getattr(self.client, method)(url or self.url, data=data, **kwargs)

    def post(self, **kwargs):
        return self.request(method='post', **kwargs)

    def put(self, **kwargs):
        return self.request(method='put', **kwargs)

    def patch(self, **kwargs):
        return self.request(method='patch', **kwargs)

    def get(self, **kwargs):
        return self.request(method='get', **kwargs)
