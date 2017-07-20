from rest_framework.routers import DefaultRouter

from shmitter.tweets.views import TweetViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)

urlpatterns = router.urls
