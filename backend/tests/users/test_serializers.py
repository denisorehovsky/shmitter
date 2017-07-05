from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict

import pytest
from nose.tools import ok_

from shmitter.users.serializers import UserSerializer
from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_data():
    return model_to_dict(f.UserFactory.build())


class TestUserSerializer:

    def test_user_serializer_hashes_password(self, user_data):
        serializer = UserSerializer(data=user_data)
        ok_(serializer.is_valid())

        user = serializer.save()
        ok_(check_password(user_data.get('password'), user.password))
