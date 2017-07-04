from rest_framework import viewsets, mixins

from .models import User
from .permissions import IsTheSameUserOrReadOnly
from .serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsTheSameUserOrReadOnly, )
