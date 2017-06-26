from unittest import mock

import pytest

from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def rf():
    """
    RequestFactory instance
    """
    return APIRequestFactory()


@pytest.fixture
def client():
    """
    A Django test client instance.
    """
    class _Client(APIClient):

        def login(self, user=None, backend='django.contrib.auth.backends.ModelBackend', **credentials):
            if user is None:
                return super().login(**credentials)

            with mock.patch('django.contrib.auth.authenticate') as authenticate:
                user.backend = backend
                authenticate.return_value = user
                return super().login(**credentials)

    return _Client()
