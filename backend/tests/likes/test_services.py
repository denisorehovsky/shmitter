import pytest
from nose.tools import eq_

from shmitter.likes import services
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_add_and_remove_like():
    user_1 = f.UserFactory()
    user_2 = f.UserFactory()
    tweet_1 = f.TweetFactory()

    services.add_like(tweet_1, user_1)
    eq_(tweet_1.likes.count(), 1)

    services.add_like(tweet_1, user_1)
    eq_(tweet_1.likes.count(), 1)

    services.add_like(tweet_1, user_2)
    eq_(tweet_1.likes.count(), 2)

    services.remove_like(tweet_1, user_2)
    eq_(tweet_1.likes.count(), 1)

    services.remove_like(tweet_1, user_2)
    eq_(tweet_1.likes.count(), 1)
