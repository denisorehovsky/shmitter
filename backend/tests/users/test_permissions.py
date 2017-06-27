from rest_framework import generics, status

import pytest
from nose.tools import eq_

from shmitter.users.models import User
from shmitter.users.permissions import IsTheSameUserOrReadOnly
from shmitter.users.serializers import UserSerializer
from .. import factories as f

pytestmark = pytest.mark.django_db


class IsTheSameUserOrReadOnlyView(generics.RetrieveUpdateAPIView):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsTheSameUserOrReadOnly, )


is_the_same_user_or_read_only_view = IsTheSameUserOrReadOnlyView.as_view()


class TestIsTheSameUserOrReadOnlyPermission:

    def test_anonymous_user_has_read_only_permissions(self, rf):
        user_1 = f.UserFactory.create()

        request = rf.get('/%s' % user_1.username)
        response = is_the_same_user_or_read_only_view(request, username=user_1.username)
        eq_(response.status_code, status.HTTP_200_OK)

        request = rf.patch('/%s' % user_1.username, {'email': 'testuser@gmail.com'})
        response = is_the_same_user_or_read_only_view(request, username=user_1.username)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_the_same_user_has_read_only_permissions(self, rf):
        user_1 = f.UserFactory.create()
        user_2 = f.UserFactory.create()

        request = rf.patch('/%s' % user_1.username, {'email': 'testuser@gmail.com'})
        request.user = user_2
        response = is_the_same_user_or_read_only_view(request, username=user_1.username)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_the_same_user_has_update_permissions(self, rf):
        user_1 = f.UserFactory.create()

        request = rf.patch('/%s' % user_1.username, {'email': 'testuser@gmail.com'})
        request.user = user_1
        response = is_the_same_user_or_read_only_view(request, username=user_1.username)
        eq_(response.status_code, status.HTTP_200_OK)
