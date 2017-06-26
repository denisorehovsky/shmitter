from django.core.exceptions import ValidationError

import pytest
from nose.tools import eq_, ok_

from shmitter.users.models import User
from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_data():
    return {
        'username': 'harrypotter',
        'email': 'harrypotter@hpmor.com',
        'full_name': 'Harry Potter',
        'password': 'I only want power so I can get books'
    }


@pytest.fixture(scope='module')
def user_obj():
    return f.UserFactory.build()


class TestUserModel:

    def test__str__(self, user_obj, mocker):
        mock_get_short_name = mocker.patch.object(user_obj, 'get_short_name')
        user_obj.__str__()
        mock_get_short_name.assert_called_once()

    def test_get_full_name(self, user_obj):
        eq_(user_obj.get_full_name(), user_obj.full_name)

    def test_get_short_name(self, user_obj):
        eq_(user_obj.get_short_name(), user_obj.username)

    def test_email_user(self, user_obj, mocker):
        mock_send_mail = mocker.patch('shmitter.users.models.send_mail')

        envelope = {
            'subject': 'test subject',
            'message': 'test message'
        }
        user_obj.email_user(**envelope)

        mock_send_mail.assert_called_once_with(
            envelope['subject'],
            envelope['message'],
            None,  # from email
            [user_obj.email]  # to
        )


class TestUserManager:

    def test_create_user(self, user_data):
        user = User.objects.create_user(**user_data)

        ok_(isinstance(user, User))
        ok_(user.pk)
        eq_(user.username, user_data['username'])
        eq_(user.email, user_data['email'])
        eq_(user.full_name, user_data['full_name'])

        ok_(user.is_active)
        ok_(user.is_staff is False)
        ok_(user.is_superuser is False)

        ok_(user.has_usable_password())
        ok_(user.check_password(user_data['password']))

    def test_create_user_normalize_email(self, user_data):
        user_data['email'] = 'harrypotter@HpMoR.CoM'
        user = User.objects.create_user(**user_data)
        eq_(user.email, 'harrypotter@hpmor.com')

    def test_create_user_with_invalid_username(self, user_data):
        user_data['username'] = 'harry potter !/'
        user = User.objects.create_user(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_with_empty_username(self, user_data):
        user_data['username'] = ''
        with pytest.raises(ValueError):
            User.objects.create_user(**user_data)

    def test_create_user_with_empty_email(self, user_data):
        user_data['email'] = ''
        with pytest.raises(ValueError):
            User.objects.create_user(**user_data)

    def test_create_user_with_empty_full_name(self, user_data):
        user_data['full_name'] = ''
        with pytest.raises(ValueError):
            User.objects.create_user(**user_data)

    def test_create_superuser(self, user_data):
        user = User.objects.create_superuser(**user_data)
        ok_(user.is_staff)
        ok_(user.is_superuser)

    def test_create_superuser_with_false_is_staff(self, user_data):
        user_data['is_staff'] = False
        with pytest.raises(ValueError):
            User.objects.create_superuser(**user_data)

    def test_create_superuser_with_false_is_superuser(self, user_data):
        user_data['is_superuser'] = False
        with pytest.raises(ValueError):
            User.objects.create_superuser(**user_data)
