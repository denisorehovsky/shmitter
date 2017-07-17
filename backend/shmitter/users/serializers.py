from rest_framework import serializers
from rest_framework.compat import is_authenticated

from friendship.models import Follow

from shmitter.likes.services import get_liked
from shmitter.tweets.models import Tweet
from shmitter.tweets.serializers import TweetSerializer
from .models import User


class UserBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'about',
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    is_follows = serializers.SerializerMethodField()
    tweets = serializers.SerializerMethodField()
    liked_tweets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'full_name',
            'about',
            'password',
            'is_follows',
            'tweets',
            'liked_tweets',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_is_follows(self, obj) -> bool:
        """
        Check if a `request.user` follows this user (`obj`).
        """
        follower = self.context.get('request').user
        if not is_authenticated(follower):
            return False
        followee = obj
        return Follow.objects.follows(
            follower=follower, followee=followee)

    def get_tweets(self, obj):
        return TweetSerializer(
            obj.tweets.all(),
            many=True,
            context=self.context
        ).data

    def get_liked_tweets(self, obj):
        return TweetSerializer(
            get_liked(Tweet, obj),
            many=True,
            context=self.context
        ).data
