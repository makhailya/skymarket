from django.urls import include, path
from rest_framework_nested import routers

from .views import AdViewSet, ReviewViewSet

# Главный роутер — регистрируем объявления
router = routers.DefaultRouter()
router.register("ads", AdViewSet, basename="ads")

# Вложенный роутер — отзывы внутри объявления
# Это создаст URL: /ads/{ad_pk}/reviews/
ads_router = routers.NestedDefaultRouter(router, "ads", lookup="ad")
ads_router.register("reviews", ReviewViewSet, basename="ad-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(ads_router.urls)),
]
