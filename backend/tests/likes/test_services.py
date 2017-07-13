import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

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


def test_get_fans():
    tweet_1 = f.TweetFactory.create()
    user_1 = f.UserFactory.create()
    user_2 = f.UserFactory.create()
    f.UserFactory.create()

    f.LikeTweetFactory.create(content_object=tweet_1, user=user_1)
    f.LikeTweetFactory.create(content_object=tweet_1, user=user_2)

    assert_queryset_equal(
        services.get_fans(tweet_1),
        [repr(user_1), repr(user_2)],
        ordered=False
    )
