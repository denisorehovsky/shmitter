from rest_framework.routers import DefaultRouter

from shmitter.users.api import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
