from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .mixins import FollowsMixin
from .models import User
from .permissions import UserPermission
from .serializers import UserSerializer


class UserViewSet(FollowsMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission, )

    @list_route(methods=['GET'])
    def me(self, request):
        me = request.user

        serializer = self.get_serializer(me)
        return Response(serializer.data)
