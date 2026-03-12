from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django
    path("admin/", admin.site.urls),
    
    # Пользователи — /users/
    path("users/", include("users.urls")),
    
    # Объявления и отзывы — /ads/
    path("", include("ads.urls")),
    
    # Авторизация через djoser — /auth/
    # Даёт нам готовые эндпоинты для регистрации и входа
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

# Это нужно чтобы Django отдавал загруженные картинки в режиме разработки
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
