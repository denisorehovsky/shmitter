import pytest

from shmitter.base.permissions import ActionPermission
from shmitter.base.permissions import (
    AllowAny as TruePermissionComponent,
    DenyAll as FalsePermissionComponent
)


@pytest.fixture
def basic_permission():
    class BasicPermission(ActionPermission):
        pass
    return BasicPermission()


@pytest.fixture
def mock_create_view(mocker):
    view = mocker.MagicMock()
    view.action = 'create'
    return view


class TestActionPermissionOperators:

    def test_NOT_operator(self):
        assert not (~TruePermissionComponent()).has_permission(None, None)
        assert (~~TruePermissionComponent()).has_permission(None, None)
        assert (~FalsePermissionComponent()).has_permission(None, None)

    def test_OR_operator(self):
        assert (TruePermissionComponent() | TruePermissionComponent()).has_permission(None, None)
        assert (TruePermissionComponent() | FalsePermissionComponent()).has_permission(None, None)
        assert (FalsePermissionComponent() | TruePermissionComponent()).has_permission(None, None)
        assert not (FalsePermissionComponent() | FalsePermissionComponent()).has_permission(None, None)

    def test_AND_operator(self):
        assert (TruePermissionComponent() & TruePermissionComponent()).has_permission(None, None)
        assert not (TruePermissionComponent() & FalsePermissionComponent()).has_permission(None, None)
        assert not (FalsePermissionComponent() & TruePermissionComponent()).has_permission(None, None)
        assert not (FalsePermissionComponent() & FalsePermissionComponent()).has_permission(None, None)

    def test_operator_chain(self):
        assert (TruePermissionComponent() & TruePermissionComponent() | FalsePermissionComponent()) \
            .has_permission(None, None)
        assert (TruePermissionComponent() & ~FalsePermissionComponent()) \
            .has_permission(None, None)


class TestActionPermissions:

    def test_list_of_components(self, basic_permission, mock_create_view):
        basic_permission.create_perms = [TruePermissionComponent(), FalsePermissionComponent()]
        assert not basic_permission.has_permission(None, mock_create_view)

    def test_component_subclass(self, basic_permission, mock_create_view):
        basic_permission.create_perms = TruePermissionComponent
        assert basic_permission.has_permission(None, mock_create_view)

    def test_invalid_permission_definition(self, basic_permission, mock_create_view):
        basic_permission.create_perms = basic_permission
        with pytest.raises(RuntimeError):
            basic_permission.has_permission(None, mock_create_view)

    def test_enough_perms(self, basic_permission, mock_create_view):
        basic_permission.enough_perms = TruePermissionComponent
        basic_permission.create_perms = FalsePermissionComponent
        assert basic_permission.has_permission(None, mock_create_view)

    def test_global_perms(self, basic_permission, mock_create_view):
        basic_permission.global_perms = FalsePermissionComponent
        basic_permission.create_perms = TruePermissionComponent
        assert not basic_permission.has_permission(None, mock_create_view)
