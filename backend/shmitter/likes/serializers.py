from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'about',
        )
