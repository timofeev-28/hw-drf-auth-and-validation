from django_filters import rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # Фильтр для диапазона дат создания
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        # Указываем поля, по которым доступна фильтрация
        fields = ["status", "created_at"]
