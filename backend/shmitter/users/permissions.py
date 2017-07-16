from shmitter.base.permissions import (
    ActionPermissionComponent, ShmitterPermission
)
from shmitter.base.permissions import AllowAny, IsAuthenticated


class IsTheSameUser(ActionPermissionComponent):

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserPermission(ShmitterPermission):
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()

    follow_perms = IsAuthenticated()
    followers_perms = AllowAny()
    following_perms = AllowAny()
