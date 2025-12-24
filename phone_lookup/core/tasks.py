from celery import shared_task
from core.services.registry_sync_service import RegistrySyncService
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_registry_task():
    """
    Celery задача для обновления реестра.
    """

    logger.info("Запуск автоматического обновления реестра...")

    try:
        full_result = RegistrySyncService.update_registry()
        for registry_result in full_result:
            logger.info(
                f'Реестр: {registry_result["registry"]}, Загружено: {registry_result["loaded"]}, Создано: {registry_result["created"]}'
            )
        return full_result
    except Exception as e:
        logger.error(f"Ошибка при обновлении реестра: {e}")
        raise