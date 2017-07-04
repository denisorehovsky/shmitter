from django.core.urlresolvers import reverse

from rest_framework import status

import pytest
from nose.tools import eq_

from shmitter.users.models import User
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestUserViewSet:

    ############################
    # Retrieve
    ############################

    def test_retrieve_user(self, client):
        user_1 = f.UserFactory.create()
        url = reverse('user-detail', kwargs={'username': user_1.username})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['username'], user_1.username)

    ############################
    # Update
    ############################

    def test_update_user(self, client):
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

    ############################
    # Permissions
    ############################

    def test_anonymous_user_has_read_only_permissions(self, client):
        user_1 = f.UserFactory.create(email='testuser-42@shmitter.com')
        data = {
            'email': 'testuser-42@gmail.com'
        }
        url = reverse('user-detail', kwargs={'username': user_1.username})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_has_all_permissions_over_himself(self, client):
        user_1 = f.UserFactory.create(email='testuser-1@shmitter.com')
        data = {
            'email': 'testuser-1@gmail.com'
        }
        url = reverse('user-detail', kwargs={'username': user_1.username})

        client.login(user_1)
        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_other_user_has_read_only_permissions(self, client):
        user_1 = f.UserFactory.create(email='testuser-1@shmitter.com')
        user_2 = f.UserFactory.create(email='testuser-2@shmitter.com')
        data = {
            'email': 'testuser@gmail.com'
        }
        url = reverse('user-detail', kwargs={'username': user_1.username})

        client.login(user_2)
        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)
