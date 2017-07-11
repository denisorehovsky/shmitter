from rest_framework import viewsets, mixins

from .models import Tweet
from .permissions import TweetPermission
from .serializers import TweetSerializer


class TweetViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (TweetPermission, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)