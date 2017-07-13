from shmitter.base.permissions import ShmitterPermission
from shmitter.base.permissions import IsAuthenticated, IsObjectOwner


class TweetPermission(ShmitterPermission):
    create_perms = IsAuthenticated()
    destroy_perms = IsObjectOwner()
    update_perms = IsObjectOwner()
    partial_update_perms = IsObjectOwner()

    like_perms = IsAuthenticated()
    unlike_perms = IsAuthenticated()
