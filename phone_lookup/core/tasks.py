from celery import shared_task
from core.services.db_sync import DbSyncService
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_registry_task():
    """
    Celery задача для обновления реестра.
    Запускается автоматически раз в сутки.
    """
    logger.info("Запуск автоматического обновления реестра...")

    try:
        result = DbSyncService.update_registry()
        logger.info(f"Реестр обновлен. Загружено: {result['loaded']}, Создано: {result['created']}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при обновлении реестра: {e}")
        raise