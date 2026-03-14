import pytest
from rest_framework import status
from rest_framework.test import APIClient

from ads.factories import AdFactory, ReviewFactory
from users.factories import UserFactory


@pytest.fixture
def api_client():
    """Клиент для отправки запросов к API"""
    return APIClient()


@pytest.fixture
def user(db):
    """Обычный пользователь"""
    return UserFactory()


@pytest.fixture
def admin(db):
    """Администратор"""
    return UserFactory(role="admin")


@pytest.fixture
def authenticated_client(api_client, user):
    """Клиент с авторизацией"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin):
    """Клиент с правами админа"""
    api_client.force_authenticate(user=admin)
    return api_client


# ==================== Тесты объявлений ====================


class TestAdList:
    """Тесты для списка объявлений"""

    def test_anyone_can_see_ads(self, db, api_client):
        """
        Неавторизованный пользователь может видеть объявления.
        Ожидаем статус 200.
        """
        AdFactory.create_batch(3)  # создаём 3 объявления
        response = api_client.get("/ads/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_search_ads_by_title(self, db, api_client):
        """
        Поиск объявлений по названию работает.
        """
        AdFactory(title="Продаю велосипед")
        AdFactory(title="Продаю машину")
        AdFactory(title="Куплю телефон")

        response = api_client.get("/ads/?search=Продаю")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2


class TestAdCreate:
    """Тесты для создания объявлений"""

    def test_authenticated_user_can_create_ad(self, db, authenticated_client):
        """
        Авторизованный пользователь может создать объявление.
        """
        data = {
            "title": "Продаю ноутбук",
            "price": 50000,
            "description": "Хороший ноутбук",
        }
        response = authenticated_client.post("/ads/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Продаю ноутбук"

    def test_anonymous_cannot_create_ad(self, db, api_client):
        """
        Неавторизованный пользователь НЕ может создать объявление.
        Ожидаем статус 401.
        """
        data = {
            "title": "Продаю ноутбук",
            "price": 50000,
        }
        response = api_client.post("/ads/", data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAdUpdate:
    """Тесты для редактирования объявлений"""

    def test_owner_can_update_ad(self, db, api_client, user):
        """
        Владелец может редактировать своё объявление.
        """
        ad = AdFactory(author=user)
        api_client.force_authenticate(user=user)

        response = api_client.patch(f"/ads/{ad.id}/", {"title": "Новый заголовок"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Новый заголовок"

    def test_other_user_cannot_update_ad(self, db, api_client, user):
        """
        Другой пользователь НЕ может редактировать чужое объявление.
        Ожидаем статус 403.
        """
        other_user = UserFactory()
        ad = AdFactory(author=other_user)
        api_client.force_authenticate(user=user)

        response = api_client.patch(f"/ads/{ad.id}/", {"title": "Хочу украсть"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_any_ad(self, db, admin_client, user):
        """
        Администратор может редактировать любое объявление.
        """
        ad = AdFactory(author=user)

        response = admin_client.patch(f"/ads/{ad.id}/", {"title": "Админ поменял"})

        assert response.status_code == status.HTTP_200_OK


class TestAdDelete:
    """Тесты для удаления объявлений"""

    def test_owner_can_delete_ad(self, db, api_client, user):
        """Владелец может удалить своё объявление"""
        ad = AdFactory(author=user)
        api_client.force_authenticate(user=user)

        response = api_client.delete(f"/ads/{ad.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_delete_any_ad(self, db, admin_client, user):
        """Администратор может удалить любое объявление"""
        ad = AdFactory(author=user)

        response = admin_client.delete(f"/ads/{ad.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT


# ==================== Тесты отзывов ====================


class TestReviews:
    """Тесты для отзывов"""

    def test_anyone_can_see_reviews(self, db, api_client):
        """Все могут видеть отзывы"""
        review = ReviewFactory()

        response = api_client.get(f"/ads/{review.ad.id}/reviews/")

        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_create_review(self, db, authenticated_client, user):
        """Авторизованный пользователь может написать отзыв"""
        ad = AdFactory()

        response = authenticated_client.post(f"/ads/{ad.id}/reviews/", {"text": "Отличное объявление!"})

        assert response.status_code == status.HTTP_201_CREATED

    def test_anonymous_cannot_create_review(self, db, api_client):
        """Неавторизованный пользователь НЕ может написать отзыв"""
        ad = AdFactory()

        response = api_client.post(f"/ads/{ad.id}/reviews/", {"text": "Хочу написать отзыв"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
