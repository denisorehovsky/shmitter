from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class UsernameOrEmailAuthentication(ModelBackend):
    """
    Authentication with either a username or an email.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        username_or_email = kwargs.get('username_or_email')
        try:
            user = User._default_manager.get(
                Q(username=username) |
                Q(username=username_or_email) |
                Q(email=username_or_email)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
