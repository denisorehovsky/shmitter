import pytest
from nose.tools import eq_, ok_
from djoser.constants import INVALID_CREDENTIALS_ERROR

from shmitter.authentication.serializers import LoginSerializer
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestLoginSerializer:

    def test_authenticate_with_valid_data(self):
        f.UserFactory.create(
            email='testuser_1@gmail.com',
            password='testuser_1')

        serializer = LoginSerializer(data={
            'username_or_email': 'testuser_1@gmail.com',
            'password': 'testuser_1'
        })
        ok_(serializer.is_valid())

    def test_validation_error_if_user_was_not_authenticated(self):
        serializer = LoginSerializer(data={
            'username_or_email': 'random_user',
            'password': 'random_password'
        })
        ok_(serializer.is_valid() is False)
        eq_(serializer.errors, {'non_field_errors': [str(INVALID_CREDENTIALS_ERROR)]})
