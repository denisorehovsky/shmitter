import pytest

from django.core.exceptions import ValidationError

from shmitter.users.validators import UsernameValidator


@pytest.fixture(scope='module')
def username_validator():
    return UsernameValidator()


class TestUsernameValidator:

    @pytest.mark.parametrize('valid_username', [
        'joe', 'René', 'ᴮᴵᴳᴮᴵᴿᴰ', 'أحمد'
    ])
    def test_valid_usernames(self, valid_username, username_validator):
        username_validator(valid_username)

    @pytest.mark.parametrize('invalid_username', [
        "o'connell", "عبد ال", "first@second", "first-second",
        "zerowidth\u200Bspace", "en\u2013dash",
    ])
    def test_invalid_usernames(self, invalid_username, username_validator):
        with pytest.raises(ValidationError):
            username_validator(invalid_username)
