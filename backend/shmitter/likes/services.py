from django.contrib.contenttypes.models import ContentType

from shmitter.likes.models import Like


def add_like(obj, user):
    """Add a like to an `obj`.

    If the `user` has already liked the `obj`, nothing will happen.

    :param obj: Any Django model instance.
    :param user: User model instance.

    :return: :class:`~shmitter.likes.models.Like` instance.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    """Remove a like from an `obj`.

    If the `user` has not liked the `obj`, nothing will happen.

    :param obj: Any Django model instance.
    :param user: User model instance.

    :return: None
    """
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    if likes.exists():
        likes.delete()
