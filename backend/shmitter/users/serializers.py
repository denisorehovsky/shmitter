from rest_framework import serializers

from shmitter.tweets.serializers import TweetSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    tweets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'full_name',
            'password',
            'tweets',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_tweets(self, obj):
        return TweetSerializer(obj.tweets.all(), many=True).data
