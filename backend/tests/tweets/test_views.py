from django.core.urlresolvers import reverse

from rest_framework import status

import pytest
from nose.tools import eq_

from shmitter.tweets.models import Tweet
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestTweetViewSet:

    ############################
    # Create
    ############################

    def test_create_tweet(self, client):
        user_1 = f.UserFactory.create()
        data = {
            'body': 'tweet body'
        }
        url = reverse('tweet-list')

        client.login(user_1)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)

    def test_created_tweet_has_an_owner(self, client):
        user_1 = f.UserFactory.create()
        data = {
            'body': 'tweet body'
        }
        url = reverse('tweet-list')

        client.login(user_1)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['owner'], user_1.username)

    ############################
    # Delete
    ############################

    def test_delete_tweet(self, client):
        tweet_1 = f.TweetFactory.create()
        tweet_1_pk = tweet_1.pk
        url = reverse('tweet-detail', kwargs={'pk': tweet_1.pk})

        response = client.delete(url)
        eq_(response.status_code, status.HTTP_204_NO_CONTENT)
        with pytest.raises(Tweet.DoesNotExist):
            Tweet.objects.get(pk=tweet_1_pk)

    ############################
    # Retrieve
    ############################

    def test_retrieve_tweet(self, client):
        tweet_1 = f.TweetFactory.create()
        url = reverse('tweet-detail', kwargs={'pk': tweet_1.pk})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], tweet_1.id)

    ############################
    # Update
    ############################

    def test_update_tweet(self, client):
        tweet_1 = f.TweetFactory.create()
        tweet_1_pk = tweet_1.pk
        data = {
            'body': 'tweet body'
        }
        url = reverse('tweet-detail', kwargs={'pk': tweet_1.pk})

        response = client.patch(url, data)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(Tweet.objects.get(pk=tweet_1_pk).body, 'tweet body')
