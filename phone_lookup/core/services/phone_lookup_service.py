from typing import Optional, Dict
from core.models import PhoneRange


class PhoneLookupService:
    """Сервис для поиска информации по номеру телефона."""

    @staticmethod
    def normalize_phone(phone: str) -> Optional[str]:
        """Очищает и нормализует номер телефона."""

        digits = ''.join(filter(str.isdigit, phone))

        # Приводим номер к формату 7XXXXXXXXXX
        if len(digits) == 11:
            if digits.startswith('7'):
                return digits
            elif digits.startswith('8'):
                return '7' + digits[1:]
        elif len(digits) == 10:
            return '7' + digits

        return None

    @staticmethod
    def lookup(phone: str) -> Optional[Dict]:
        """
        Ищет информацию по номеру телефона.
        Возвращает словарь с данными или None если не найден.
        """

        normalized = PhoneLookupService.normalize_phone(phone)

        if not normalized:
            return None

        try:
            full_number = int(normalized)
        except ValueError:
            return None

        abc = int(normalized[1:4])
        suffix = full_number - 70000000000 - abc * 10000000

        phone_range = PhoneRange.objects.filter(
            abc=abc,
            start_range__lte=suffix,
            end_range__gte=suffix
        ).first()

        if not phone_range:
            return None

        return {
            'phone': phone,
            'normalized': normalized,
            'operator': phone_range.operator,
            'region': phone_range.region or '',
            'inn': phone_range.inn or '',
        }