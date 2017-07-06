from rest_framework.routers import DefaultRouter

from shmitter.tweets.views import TweetViewSet
from shmitter.users.views import UserViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'users', UserViewSet)
