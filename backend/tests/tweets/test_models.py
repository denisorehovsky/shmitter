import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

from shmitter.tweets.models import Tweet
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestTweetModel:

    def test__str__(self):
        tweet_1 = f.TweetFactory()
        eq_(tweet_1.__str__(), 'Tweet {}'.format(tweet_1.id))

    def test_body_length_should_be_less_than_or_equal_to_140(self):
        f.TweetFactory(body='H' * 140)
        with pytest.raises(Exception):
            f.TweetFactory(body='H' * 150)

    def test_ordering(self):
        tweet_1 = f.TweetFactory()
        tweet_2 = f.TweetFactory()

        assert_queryset_equal(
            Tweet.objects.all(),
            [repr(tweet_2), repr(tweet_1)]
        )

    def test_total_likes(self, mocker):
        tweet_1 = f.TweetFactory()
        likes_mock = mocker.patch('shmitter.tweets.models.Tweet.likes')

        tweet_1.total_likes
        likes_mock.count.assert_called_once_with()

    def test_total_retweets(self, mocker):
        tweet_1 = f.TweetFactory()
        retweets_mock = mocker.patch('shmitter.tweets.models.Tweet.retweeted_by')

        tweet_1.total_retweets
        retweets_mock.count.assert_called_once_with()
