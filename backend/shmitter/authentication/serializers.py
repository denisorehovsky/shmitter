from django.contrib.auth import authenticate

from rest_framework import serializers

from djoser import constants


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=False)
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    default_error_messages = {
        'invalid_credentials': constants.INVALID_CREDENTIALS_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(
            username_or_email=attrs.get('username_or_email'),
            password=attrs.get('password')
        )
        if self.user:
            return attrs
        else:
            raise serializers.ValidationError(
                self.default_error_messages['invalid_credentials']
            )
