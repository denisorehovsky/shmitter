from django.contrib.contenttypes.models import ContentType

import factory


class LikeFactory(factory.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


class LikeTweetFactory(LikeFactory):
    user = factory.SubFactory('tests.factories.UserFactory')
    content_object = factory.SubFactory('tests.factories.TweetFactory')

    class Meta:
        model = 'likes.Like'


class TweetFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory('tests.factories.UserFactory')
    body = factory.Sequence(lambda n: 'body-{0}'.format(n))

    class Meta:
        model = 'tweets.Tweet'


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user_{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    full_name = factory.Sequence(lambda n: 'full-name-{0}'.format(n))
    about = factory.Sequence(lambda n: 'about-{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )
