from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import services


class RetweetsMixin:

    @detail_route(methods=['POST'])
    def retweet(self, request, pk=None):
        obj = self.get_object()

        services.retweet(obj, user=request.user)
        return Response()

    @detail_route(methods=['POST'])
    def undo_retweet(self, request, pk=None):
        obj = self.get_object()

        services.undo_retweet(obj, user=request.user)
        return Response()
