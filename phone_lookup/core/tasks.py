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
        result = RegistrySyncService.update_registry()
        logger.info(f"Реестр обновлен. Загружено: {result['loaded']}, Создано: {result['created']}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при обновлении реестра: {e}")
        raise