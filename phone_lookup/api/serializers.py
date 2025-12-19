from rest_framework import serializers


class PhoneLookupSerializer(serializers.Serializer):
    """Сериализатор для запроса поиска номера."""

    phone = serializers.CharField(
        max_length=20,
        required=True,
        help_text='Номер телефона в любом формате (MSISDN, +7, 8)'
    )

    def validate_phone(self, value):
        """Валидация номера по длинне."""

        digits = ''.join(filter(str.isdigit, value))

        if len(digits) < 10:
            raise serializers.ValidationError('Номер слишком короткий')

        return value