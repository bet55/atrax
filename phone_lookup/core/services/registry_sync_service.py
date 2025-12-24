import csv
import requests
from django.db import transaction
from core.models import PhoneRange


class RegistrySyncService:
    CSV_MAP = {
        'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv': '3xx',
        'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv': '4xx',
        'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv': '8xx',
        'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv': '9xx',
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    @classmethod
    def _parse_row(cls, row: dict) -> dict | None:
        """Парсит строку CSV в формат для БД."""

        try:
            return {
                'registry_source': cls.current_registry_source,
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
    def _parse_csv(cls, csv_data: str) -> list[dict]:
        """Парсит весь CSV."""

        reader = csv.DictReader(csv_data.splitlines(), delimiter=';')

        data = []
        for row in reader:
            item = cls._parse_row(row)
            if item:
                data.append(item)

        return data

    @classmethod
    def _replace_phone_ranges(cls, data: list[dict]) -> dict:
        """Заменяет весь реестр новыми данными."""

        with transaction.atomic():
            # Удаляем все старые записи
            PhoneRange.objects.filter(
                registry_source = cls.current_registry_source,
            ).delete()

            # Создаем новые пачками
            batch_size = 1000
            created = 0

            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                phone_ranges = [PhoneRange(**item) for item in batch]
                PhoneRange.objects.bulk_create(phone_ranges)
                created += len(batch)

        return {
            'registry': cls.current_registry_source,
            'loaded': len(data),
            'created': created,
        }

    @classmethod
    def update_registry(cls) -> list[dict]:
        """Загружает CSV реестр и полностью обновляет БД."""

        result_info = []

        for url, registry_source in cls.CSV_MAP.items():
            # Запоминаем с каким реестром работаем
            cls.current_registry_source = registry_source

            # Скачиваем CSV
            csv = cls._download_csv(
                url,
                cls.HEADERS,
            )

            # Парсим CSV
            data = cls._parse_csv(
                csv
            )

            # Обновляем БД
            result_info.append(
                cls._replace_phone_ranges(data)
            )

        return result_info
