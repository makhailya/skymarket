from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Ad, Review
from .permissions import IsOwnerOrAdmin
from .serializers import AdDetailSerializer, AdSerializer, ReviewSerializer


class AdPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для объявлений.
    Автоматически создаёт все эндпоинты:

    GET    /ads/        — список всех объявлений
    POST   /ads/        — создать объявление
    GET    /ads/{id}/   — одно объявление
    PATCH  /ads/{id}/   — обновить объявление
    DELETE /ads/{id}/   — удалить объявление
    GET    /ads/me/     — мои объявления
    """

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title"]  # поиск по названию

    def get_serializer_class(self):
        """
        Для детальной страницы используем подробный сериализатор,
        для списка — краткий.
        """
        if self.action == "retrieve":
            return AdDetailSerializer
        return AdSerializer

    def get_permissions(self):
        """
        Разные права для разных действий.

        Просматривать могут все.
        Создавать — только авторизованные.
        Редактировать/удалять — только владелец или админ.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        При создании объявления автоматически
        подставляем текущего пользователя как автора.
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Дополнительный эндпоинт GET /ads/me/
        Возвращает объявления текущего пользователя.
        """
        my_ads = Ad.objects.filter(author=request.user)
        serializer = AdSerializer(my_ads, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для отзывов.

    GET    /ads/{ad_id}/reviews/      — все отзывы к объявлению
    POST   /ads/{ad_id}/reviews/      — написать отзыв
    PATCH  /ads/{ad_id}/reviews/{id}/ — редактировать отзыв
    DELETE /ads/{ad_id}/reviews/{id}/ — удалить отзыв
    """

    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Возвращаем только отзывы к конкретному объявлению.
        ad_id берём из URL.
        """
        return Review.objects.filter(ad_id=self.kwargs["ad_pk"])

    def perform_create(self, serializer):
        """
        При создании автоматически подставляем
        текущего пользователя и объявление из URL.
        """
        ad = Ad.objects.get(pk=self.kwargs["ad_pk"])
        serializer.save(author=self.request.user, ad=ad)
