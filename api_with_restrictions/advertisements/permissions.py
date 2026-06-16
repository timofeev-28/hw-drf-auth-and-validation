from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Разрешение, которое проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Методы чтения (GET, HEAD, OPTIONS) доступны всем
        if request.method in SAFE_METHODS:
            return True
        # Изменять и удалять может только создатель
        return request.user == obj.creator
