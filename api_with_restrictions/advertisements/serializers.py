from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context.get("request")

        # Проверку имеет смысл проводить только при методах, изменяющих данные
        if request and request.method in ("POST", "PUT", "PATCH"):
            user = request.user
            status = data.get("status")

            # Если статус не передан в запросе, берем текущий статус объекта
            # (при обновлении) или предполагаем OPEN (при создании)
            if self.instance:
                if status is None:
                    status = self.instance.status
            else:
                if status is None:
                    status = "OPEN"  # Замените на Advertisement.Status.OPEN, если у вас Enum/Choices

            # Проверяем лимит только если итоговый статус — OPEN
            if status == "OPEN":
                # Считаем количество открытых объявлений у текущего пользователя
                open_ads = Advertisement.objects.filter(
                    creator=user, status="OPEN"
                )

                # Если это обновление, исключаем текущее объявление из подсчета
                if self.instance:
                    open_ads = open_ads.exclude(pk=self.instance.pk)

                if open_ads.count() >= 10:
                    raise serializers.ValidationError(
                        "У пользователя не может быть больше 10 открытых объявлений."
                    )

        return data
