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

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context.get("request")

        if request and request.method in ("POST", "PUT", "PATCH"):
            user = request.user
            status = data.get("status")

            if self.instance:
                if status is None:
                    status = self.instance.status
            else:
                if status is None:
                    status = "OPEN"

            if status == "OPEN":
                open_ads = Advertisement.objects.filter(
                    creator=user, status="OPEN"
                )

                if self.instance:
                    open_ads = open_ads.exclude(pk=self.instance.pk)

                if open_ads.count() >= 10:
                    raise serializers.ValidationError(
                        "У пользователя не может быть больше 10 открытых объявлений."
                    )

        return data
