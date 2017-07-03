from django.contrib.auth import authenticate
from django.test import override_settings

import pytest
from nose.tools import eq_

from .. import factories as f

pytestmark = pytest.mark.django_db


@override_settings(AUTHENTICATION_BACKENDS=['shmitter.authentication.backends.UsernameOrEmailAuthentication'])
def test_username_or_email_authentication():
    user_credentials = {
        'username': 'testuser42',
        'email': 'testuser42@gmail.com',
        'password': 'testuser'
    }
    user_1 = f.UserFactory.create(**user_credentials)

    eq_(authenticate(username=user_credentials['username'], password=user_credentials['password']),
        user_1)
    eq_(authenticate(username_or_email=user_credentials['username'], password=user_credentials['password']),
        user_1)
    eq_(authenticate(username_or_email=user_credentials['email'], password=user_credentials['password']),
        user_1)

    eq_(authenticate(username=user_credentials['email'], password=user_credentials['password']),
        None)
    eq_(authenticate(username=user_credentials['username'], password='bad_password'),
        None)

    user_1.is_active = False
    user_1.save()
    eq_(authenticate(username=user_credentials['username'], password=user_credentials['password']),
        None)
