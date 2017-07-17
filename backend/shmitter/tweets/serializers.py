from rest_framework import serializers

from shmitter.likes import services
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'owner',
            'body',
            'is_fan',
            'total_likes',
            'created',
        )

    def get_is_fan(self, obj):
        """
        Check if a `request.user` has liked a tweet.
        """
        user = self.context.get('request').user
        return services.is_fan(obj, user)
