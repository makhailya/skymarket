from django.conf import settings
from django.db import models


class Ad(models.Model):
    """
    Модель объявления.
    Как карточка товара на Авито.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        default=0,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="ads/",
        verbose_name="Фото",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="ads",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    """
    Модель отзыва к объявлению.
    Как комментарий под товаром.
    """

    text = models.TextField(
        verbose_name="Текст отзыва",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="reviews",
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        verbose_name="Объявление",
        related_name="reviews",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Отзыв от {self.author} на {self.ad}"
