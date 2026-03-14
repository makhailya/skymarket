import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для создания тестовых пользователей.
    Каждый раз создаёт уникального пользователя.
    """

    class Meta:
        model = User

    # factory.Sequence гарантирует уникальность — user1@test.com, user2@test.com...
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    role = User.USER
    is_active = True
