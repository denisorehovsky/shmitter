from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from rest_framework_jwt.compat import Serializer as JWTSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class JSONWebTokenSerializer(JWTSerializer):
    username_or_email = serializers.CharField(required=False)
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    def validate(self, attrs):
        credentials = {
            'username_or_email': attrs.get('username_or_email'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username_or_email" and "password".')
            raise serializers.ValidationError(msg)
