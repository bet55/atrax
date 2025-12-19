import csv
import requests
from django.db import transaction
from core.models import PhoneRange


class RegistrySyncService:
    CSV_URL = 'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    @staticmethod
    def _parse_row(row: dict) -> dict | None:
        """Парсит строку CSV в формат для БД."""

        try:
            return {
                'abc': int(row['АВС/ DEF']),
                'start_range': int(row['От']),
                'end_range': int(row['До']),
                'capacity': int(row['Емкость']) if row['Емкость'] else None,
                'operator': row['Оператор'].strip(),
                'region': row['Регион'].strip() if row['Регион'] else None,
                'territory': row['Территория по ГАР'].strip() if row.get('Территория по ГАР') else None,
                'inn': row['ИНН'].strip() if row['ИНН'] else None,
            }
        except (KeyError, ValueError):
            None

    @staticmethod
    def _download_csv(url: str, headers: dict[str, str]) -> str:
        """Загружает CSV."""

        try:
            response = requests.get(
                url=url,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.content.decode('utf-8-sig')
        except requests.exceptions.RequestException:
            pass

    @classmethod
    def _parse_csv(cls, data: str) -> list[dict]:
        """Парсит весь CSV."""

        reader = csv.DictReader(data.splitlines(), delimiter=';')

        data = []
        for row in reader:
            item = cls._parse_row(row)
            if item:
                data.append(item)

        return data

    @staticmethod
    def _replace_phone_ranges(data: list[dict]) -> dict:
        """Заменяет весь реестр новыми данными."""

        with transaction.atomic():
            # Удаляем все старые записи
            PhoneRange.objects.all().delete()

            # Создаем новые пачками
            batch_size = 1000
            created = 0

            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                phone_ranges = [PhoneRange(**item) for item in batch]
                PhoneRange.objects.bulk_create(phone_ranges)
                created += len(batch)

        return {
            'loaded': len(data),
            'created': created,
        }

    @classmethod
    def update_registry(cls) -> dict:
        """Загружает CSV реестр и полностью обновляет БД."""

        # Скачиваем CSV
        csv = cls._download_csv(
            cls.CSV_URL,
            cls.HEADERS,
        )

        # Парсим CSV
        data = cls._parse_csv(csv)

        # Обновляем БД
        result = cls._replace_phone_ranges(data)

        return result
