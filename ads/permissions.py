from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Право доступа: только владелец объекта или админ.

    Например: редактировать объявление может только
    тот кто его создал, или администратор.
    """

    def has_object_permission(self, request, view, obj):
        # Если у объекта есть поле author — проверяем его
        if hasattr(obj, "author"):
            return obj.author == request.user or request.user.is_admin

        # Если объект сам является пользователем
        return obj == request.user or request.user.is_admin
