from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения пользователя.
    Используется когда нужно показать данные о пользователе.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "image",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля.
    Пользователь не должен менять email и роль сам.
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "image",
        ]

