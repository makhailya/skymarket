from django.urls import path
from .views import UserDetailView

urlpatterns = [
    # GET  /users/me/ — посмотреть свой профиль
    # PATCH /users/me/ — обновить свой профиль
    path("me/", UserDetailView.as_view(), name="user-detail"),
]