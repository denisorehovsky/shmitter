from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from friendship.models import Follow

from .models import User
from .permissions import UserPermission
from .serializers import UserSerializer, UserBasicInfoSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission, )

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
