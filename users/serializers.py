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

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя через Djoser.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
        ]

    def create(self, validated_data):
        # Извлекаем email и пароль, чтобы они не дублировались в **validated_data
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        
        # Создаем пользователя через менеджер (он хэширует пароль)
        user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data
        )
        
        # Явно активируем пользователя
        user.is_active = True
        user.save()
        
        return user

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
