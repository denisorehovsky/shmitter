from rest_framework.decorators import detail_route
from rest_framework.response import Response

from friendship.models import Follow

from .serializers import UserBasicInfoSerializer


class FollowsMixin:

    @detail_route(methods=['POST'])
    def follow(self, request, *args, **kwargs):
        followee = self.get_object()
        follower = request.user

        Follow.objects.add_follower(follower=follower, followee=followee)
        return Response()

    @detail_route(methods=['POST'])
    def unfollow(self, request, *args, **kwargs):
        followee = self.get_object()
        follower = request.user

        Follow.objects.remove_follower(follower=follower, followee=followee)
        return Response()

    @detail_route(methods=['GET'])
    def followers(self, request, *args, **kwargs):
        user = self.get_object()

        followers = Follow.objects.followers(user)
        serializer = UserBasicInfoSerializer(followers, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET'])
    def following(self, request, *args, **kwargs):
        user = self.get_object()

        following = Follow.objects.following(user)
        serializer = UserBasicInfoSerializer(following, many=True)
        return Response(serializer.data)
