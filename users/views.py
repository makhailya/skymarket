from rest_framework import generics, permissions
from .serializers import UserSerializer, UserUpdateSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование своего профиля.
    GET  /users/me/ — посмотреть профиль
    PATCH /users/me/ — обновить профиль
    """

    permission_classes = [permissions.IsAuthenticated]  # только авторизованные

    def get_object(self):
        # Всегда возвращаем текущего пользователя
        return self.request.user

    def get_serializer_class(self):
        # GET запрос — показываем полный профиль
        # PATCH запрос — используем сериализатор для обновления
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserSerializer
