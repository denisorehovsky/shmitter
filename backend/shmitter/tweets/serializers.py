from rest_framework import serializers

from shmitter.likes import services as likes_services
from .models import Tweet
from . import services as tweets_services


class TweetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    is_fan = serializers.SerializerMethodField()
    is_retweeted = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'owner',
            'body',
            'is_fan',
            'is_retweeted',
            'total_likes',
            'total_retweets',
            'created',
        )

    def get_is_fan(self, obj) -> bool:
        """
        Check if a `request.user` has liked this tweet (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_is_retweeted(self, obj) -> bool:
        """
        Check if a `request.user` has retweeted this tweet (`obj`).
        """
        user = self.context.get('request').user
        return tweets_services.is_retweeted(obj, user)
