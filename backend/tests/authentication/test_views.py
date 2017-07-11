from django.core.urlresolvers import reverse

from rest_framework import status

import pytest
from nose.tools import eq_, ok_

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_login(client):
    user_1 = f.UserFactory.create(password='password')
    data = {
        'username_or_email': user_1.email,
        'password': 'password'
    }
    url = reverse('login')

    response = client.post(url, data)
    eq_(response.status_code, status.HTTP_200_OK)
    ok_('token' in response.data)
