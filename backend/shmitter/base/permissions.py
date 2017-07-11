import abc
import functools
import operator

from rest_framework.compat import is_authenticated


##############################
# Base
##############################


class BasePermission(metaclass=abc.ABCMeta):
    """
    A base class from which all permission classes should inherit.
    """

    @abc.abstractmethod
    def has_permission(self, request, view):
        pass

    @abc.abstractmethod
    def has_object_permission(self, request, view, obj):
        pass


class BaseComponent(BasePermission, metaclass=abc.ABCMeta):
    """
    A base class from which all component classes should inherit.
    """

    def __invert__(self):
        return Not(self)

    def __or__(self, component):
        return Or(self, component)

    def __and__(self, component):
        return And(self, component)


class EvaluatePermissionsMixin:

    def has_permission(self, request, view):
        return self.evaluate_permissions('has_permission', request, view)

    def has_object_permission(self, request, view, obj):
        return self.evaluate_permissions('has_object_permission', request, view, obj)


##############################
# Operators
##############################


class Not(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, component):
        self.component = component

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return not getattr(self.component, permission_name)(*args, **kwargs)


class Or(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, *components):
        self.components = components

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return any(getattr(component, permission_name)(*args, **kwargs)
                   for component in self.components)


class And(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, *components):
        self.components = components

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return all(getattr(component, permission_name)(*args, **kwargs)
                   for component in self.components)


##############################
# Components
##############################


class ActionPermissionComponent(BaseComponent):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(ActionPermissionComponent):
    """
    Allow any access.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class DenyAll(ActionPermissionComponent):
    """
    Deny any access.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAuthenticated(ActionPermissionComponent):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminUser(ActionPermissionComponent):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user) and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUser(ActionPermissionComponent):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user) and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsObjectOwner(ActionPermissionComponent):
    """
    Allow access only to users that own `obj`.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


##############################
# Permissions
##############################


class ActionPermission(EvaluatePermissionsMixin, BasePermission):
    enough_perms = None
    global_perms = None

    create_perms = AllowAny()
    destroy_perms = AllowAny()
    list_perms = AllowAny()
    retrieve_perms = AllowAny()
    update_perms = AllowAny()
    partial_update_perms = AllowAny()

    def _validate_permissions(self, perms):
        if isinstance(perms, BaseComponent):
            return perms
        elif isinstance(perms, (tuple, list)):
            # If we have a list of components, then we need to convert them
            # into one single component using `And` operator.
            return functools.reduce(operator.and_, perms)
        elif issubclass(perms, BaseComponent):
            return perms()
        else:
            raise RuntimeError('Invalid permission definition')

    def _get_action_permissions(self, action):
        action_perms = getattr(self, '{}_perms'.format(action))
        action_perms = self._validate_permissions(action_perms)
        return action_perms

    def _get_enough_permissions(self):
        enough_perms = self.enough_perms
        if enough_perms:
            enough_perms = self._validate_permissions(enough_perms)
            return enough_perms

    def _get_global_permissions(self):
        global_perms = self.global_perms
        if global_perms:
            global_perms = self._validate_permissions(global_perms)
            return global_perms

    def _get_required_permissions(self, action):
        perms = self._get_action_permissions(action)

        global_perms = self._get_global_permissions()
        if global_perms is not None:
            perms = global_perms & perms

        enough_perms = self._get_enough_permissions()
        if enough_perms is not None:
            perms = enough_perms | perms

        return perms

    def evaluate_permissions(self, permission_name, request, view, *args, **kwargs):
        perms = self._get_required_permissions(view.action)
        return getattr(perms, permission_name)(request, view, *args, **kwargs)


class ShmitterPermission(ActionPermission):
    enough_perms = IsSuperUser()
