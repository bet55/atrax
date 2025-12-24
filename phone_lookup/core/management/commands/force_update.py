from django.core.management.base import BaseCommand
from core.services.registry_sync_service import RegistrySyncService


class Command(BaseCommand):
    help = 'Обновляет реестр номеров'

    def handle(self, *args, **options):
        self.stdout.write('Начниаем обновление реестра')
        full_result = RegistrySyncService.update_registry()
        for registry_result in full_result:
            self.stdout.write(f'Реестр: {registry_result["registry"]}, Загружено: {registry_result["loaded"]}, Создано: {registry_result["created"]}')
