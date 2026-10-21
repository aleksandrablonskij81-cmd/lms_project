from rest_framework.permissions import BasePermission


def is_moderator(user) -> bool:
    return user.is_authenticated and user.groups.filter(name="Модератор").exists()


class IsNotModerator(BasePermission):
    """Обычный пользователь, но не модератор."""

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and not is_moderator(request.user)


class IsOwnerOrModerator(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner_id == request.user.id or is_moderator(request.user)


class IsOwnerAndNotModerator(BasePermission):
    """Удалять объект может только его владелец, но не модератор."""

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and not is_moderator(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner_id == request.user.id