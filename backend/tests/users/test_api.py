from django.core.urlresolvers import reverse

from rest_framework import status

import pytest
from nose.tools import eq_

from shmitter.users.models import User
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_retrieve_user(client):
    user_1 = f.UserFactory.create()
    url = reverse('user-detail', kwargs={'username': user_1.username})

    response = client.get(url)
    eq_(response.status_code, status.HTTP_200_OK)
    eq_(response.data['username'], user_1.username)


def test_update_user(client):
    user_1 = f.UserFactory.create(email='testuser-1@shmitter.com')
    user_1_pk = user_1.pk
    data = {
        'email': 'testuser-1@gmail.com'
    }
    url = reverse('user-detail', kwargs={'username': user_1.username})

    client.login(user_1)
    response = client.patch(url, data)
    eq_(response.status_code, status.HTTP_200_OK)
    eq_(User.objects.get(pk=user_1_pk).email, 'testuser-1@gmail.com')
