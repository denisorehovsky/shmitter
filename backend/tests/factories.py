import factory


class TweetFactory(factory.django.DjangoModelFactory):
    body = factory.Sequence(lambda n: 'body-{0}'.format(n))

    class Meta:
        model = 'tweets.Tweet'


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )
