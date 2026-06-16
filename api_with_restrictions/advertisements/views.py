from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    # Подключаем бэкенд фильтрации и класс фильтров
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """
        Переопределяем права доступа для различных действий (actions).
        """
        if self.action == "create":
            # Создавать могут только авторизованные пользователи
            self.permission_classes = [IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            # Обновлять и удалять может только авторизованный пользователь,
            # который является владельцем объекта (IsOwner)
            self.permission_classes = [IsAuthenticated, IsOwner]

        else:
            # Для просмотра (list, retrieve) авторизация не нужна
            self.permission_classes = [AllowAny]

        return super().get_permissions()
