from rest_framework import serializers


class PhoneLookupSerializer(serializers.Serializer):
    """Сериализатор для запроса поиска номера."""
    phone = serializers.CharField(
        max_length=20,
        required=True,
        help_text='Номер телефона в любом формате (MSISDN, +7, 8, etc)'
    )

    def validate_phone(self, value):
        """Простая валидация номера."""
        # Оставляем только цифры
        digits = ''.join(filter(str.isdigit, value))

        # Проверяем минимальную длину
        if len(digits) < 10:
            raise serializers.ValidationError('Номер слишком короткий')

        return value