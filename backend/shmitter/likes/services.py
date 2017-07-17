from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework.compat import is_authenticated

from shmitter.likes.models import Like

User = get_user_model()


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


def get_liked(model, user_or_id):
    """Get the objects liked by a user.

    :param model: Show only objects of this kind. Can be any Django model class.
    :param user_or_id: User model instance or id.

    :return: Queryset of objects liked by a user.
    """
    obj_type = ContentType.objects.get_for_model(model)
    if isinstance(user_or_id, get_user_model()):
        user_id = user_or_id.id
    else:
        user_id = user_or_id

    return model.objects.filter(
        likes__content_type=obj_type, likes__user_id=user_id)


def is_fan(obj, user):
    """Check whether a `user` has liked an `obj` or not.

    :param obj: Any Django model instance.
    :param user: User model instance.

    :return: True or False
    """
    if not is_authenticated(user):
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return True if likes.exists() else False


def get_fans(obj):
    """Get the users which liked an `obj`.

    :param obj: Any Django model instance.

    :return: Queryset of users.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)
