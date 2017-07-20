import pytest
from nose.tools import eq_, ok_
from django_nose.tools import assert_queryset_equal

from shmitter.tweets import services
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_is_retweeted():
    user_1 = f.UserFactory()
    user_2 = f.UserFactory()
    tweet_1 = f.TweetFactory(retweeted_by=[user_1])

    ok_(services.is_retweeted(tweet_1, user_1))
    ok_(services.is_retweeted(tweet_1, user_2) is False)


def test_retweet():
    user_1 = f.UserFactory()
    user_2 = f.UserFactory()
    tweet_1 = f.TweetFactory(retweeted_by=[user_1, user_2])

    services.retweet(tweet_1, user_1)
    services.retweet(tweet_1, user_2)
    assert_queryset_equal(
        tweet_1.retweeted_by.all(),
        [repr(user_1), repr(user_2)],
        ordered=False
    )


def test_undo_retweet():
    user_1 = f.UserFactory()
    tweet_1 = f.TweetFactory(retweeted_by=[user_1])

    services.undo_retweet(tweet_1, user_1)
    eq_(tweet_1.retweeted_by.count(), 0)
