from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка объявлений.
    Показываем краткую информацию.
    """

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "image",
            "author",
            "created_at",
        ]
        read_only_fields = ["author", "created_at"]


class AdDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной страницы объявления.
    Показываем полную информацию включая автора.
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "image",
            "author",
            "created_at",
        ]
        read_only_fields = ["author", "created_at"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов.
    """

    author_first_name = serializers.CharField(
        source="author.first_name",
        read_only=True,
    )
    author_last_name = serializers.CharField(
        source="author.last_name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "text",
            "author",
            "author_first_name",
            "author_last_name",
            "ad",
            "created_at",
        ]
        read_only_fields = ["author", "ad", "created_at"]
