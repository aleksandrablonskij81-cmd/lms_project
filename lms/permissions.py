from rest_framework import permissions


class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"🔍 has_permission: user={request.user.email}, action={view.action}, method={request.method}")
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        if request.user.groups.filter(name='Модератор').exists():
            if view.action in ['create', 'destroy']:
                return False
            return True
        return True

    def has_object_permission(self, request, view, obj):
        print(f"🔍 has_object_permission: user={request.user.email}, obj.owner={getattr(obj, 'owner', None)}, method={request.method}")
        if request.user.groups.filter(name='Модератор').exists():
            return True
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        return request.method in permissions.SAFE_METHODS