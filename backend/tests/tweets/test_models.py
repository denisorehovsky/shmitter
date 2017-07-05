import pytest
from django_nose.tools import assert_queryset_equal

from shmitter.tweets.models import Tweet
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestTweetModel:

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
