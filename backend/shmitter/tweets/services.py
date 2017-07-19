from rest_framework.compat import is_authenticated

from .models import Tweet


def get_total_number_of_retweets(tweet) -> int:
    """Get total number of retweets of the `tweet`.

    :param tweet: :class:`~shmitter.tweets.models.Tweet` instance.
    """
    return tweet.retweeted_by.count()


def is_retweeted(tweet, user) -> bool:
    """Check whether a `user` has retweeted the `tweet` or not.

    :param tweet: :class:`~shmitter.tweets.models.Tweet` instance.
    :param user: User model instance.

    :return: True or False
    """
    if not is_authenticated(user):
        return False
    tweets = Tweet.objects.filter(id=tweet.id, retweeted_by=user)
    return True if tweets.exists() else False


def retweet(tweet, user) -> None:
    """Retweet the `tweet`.

    :param tweet: :class:`~shmitter.tweets.models.Tweet` instance.
    :param user: User model instance.
    """
    tweet.retweeted_by.add(user)


def undo_retweet(tweet, user) -> None:
    """Undo the `tweet` retweet.

    :param tweet: :class:`~shmitter.tweets.models.Tweet` instance.
    :param user: User model instance.
    """
    tweet.retweeted_by.remove(user)
