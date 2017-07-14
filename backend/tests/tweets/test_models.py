import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

from shmitter.tweets.models import Tweet
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestTweetModel:

    def test__str__(self):
        tweet_1 = f.TweetFactory.create()
        eq_(tweet_1.__str__(), 'Tweet {}'.format(tweet_1.id))

    def test_body_length_should_be_less_than_or_equal_to_140(self):
        f.TweetFactory.create(body='H' * 140)
        with pytest.raises(Exception):
            f.TweetFactory.create(body='H' * 150)

    def test_ordering(self):
        tweet_1 = f.TweetFactory.create()
        tweet_2 = f.TweetFactory.create()

        assert_queryset_equal(
            Tweet.objects.all(),
            [repr(tweet_2), repr(tweet_1)]
        )
