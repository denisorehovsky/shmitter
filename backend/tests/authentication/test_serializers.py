import pytest
from nose.tools import eq_, ok_

from shmitter.authentication.serializers import JSONWebTokenSerializer
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestJSONWebTokenSerializer:

    def test_authenticate_with_valid_data(self):
        f.UserFactory.create(
            email='testuser_1@gmail.com',
            password='testuser_1')

        serializer = JSONWebTokenSerializer(data={
            'username_or_email': 'testuser_1@gmail.com',
            'password': 'testuser_1'
        })
        ok_(serializer.is_valid())

    def test_validation_error_if_credentials_are_not_valid(self):
        serializer = JSONWebTokenSerializer(data={
            'username_or_email': 'random_user',
            'password': 'random_password'
        })
        ok_(serializer.is_valid() is False)
        eq_(serializer.errors, {'non_field_errors': ['Unable to log in with provided credentials.']})

    def test_validation_error_if_all_fields_were_not_filled(self):
        serializer = JSONWebTokenSerializer(data={
            'password': 'random_password'
        })
        ok_(serializer.is_valid() is False)
        eq_(serializer.errors, {'non_field_errors': ['Must include "username_or_email" and "password".']})
