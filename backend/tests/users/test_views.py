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

    def test_user_has_tweets(self, client):
        user_1 = f.UserFactory.create()
        f.TweetFactory.create(owner=user_1)
        f.TweetFactory.create(owner=user_1)
        url = reverse('user-detail', kwargs={'username': user_1.username})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['tweets']), 2)

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

    def test_user_can_only_update_himself(self, client):
        user_1 = f.UserFactory.create()
        user_2 = f.UserFactory.create(email='testuser-42@shmitter.com')
        data = {
            'email': 'testuser-42@gmail.com'
        }
        url = reverse('user-detail', kwargs={'username': user_2.username})

        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.login(user_1)
        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

        client.login(user_2)
        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_200_OK)
