from django.core.management.base import BaseCommand
from core.services.registry_sync_service import RegistrySyncService


class Command(BaseCommand):
    help = 'Обновляет реестр номеров'

    def handle(self, *args, **options):
        self.stdout.write('Начниаем обновление реестра')
        result = RegistrySyncService.update_registry()
        self.stdout.write(f'Загружено: {result["loaded"]}, Создано: {result["created"]}')
