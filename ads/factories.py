import factory
from .models import Ad, Review
from users.factories import UserFactory


class AdFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для создания тестовых объявлений.
    """

    class Meta:
        model = Ad

    title = factory.Faker("sentence", nb_words=4, locale="ru_RU")
    price = factory.Faker("random_int", min=100, max=100000)
    description = factory.Faker("paragraph", locale="ru_RU")
    author = factory.SubFactory(UserFactory)  # автоматически создаёт пользователя


class ReviewFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для создания тестовых отзывов.
    """

    class Meta:
        model = Review

    text = factory.Faker("paragraph", locale="ru_RU")
    author = factory.SubFactory(UserFactory)
    ad = factory.SubFactory(AdFactory)