from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import FanSerializer
from . import services


class LikedMixin:
    """
    Like and unlike a model instance.
    """

    @detail_route(methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()

        services.add_like(obj, user=request.user)
        return Response()

    @detail_route(methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()

        services.remove_like(obj, user=request.user)
        return Response()


class FansMixin:
    """
    Get the users which liked a model instance.
    """

    @detail_route(methods=['GET'])
    def fans(self, request, pk=None):
        obj = self.get_object()

        users = services.get_fans(obj)
        serializer = FanSerializer(users, many=True)
        return Response(serializer.data)
