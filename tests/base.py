from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response


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
        **kwargs
    ) -> Response:
        return getattr(self.client, method)(url or self.url, data=data, **kwargs)

    def post(self, **kwargs):
        return self.request(method='post', **kwargs)

    def put(self, **kwargs):
        return self.request(method='put', **kwargs)

    def get(self, **kwargs):
        return self.request(method='get', **kwargs)