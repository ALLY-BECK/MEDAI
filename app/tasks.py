import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task
def dummy_task(message):
    logger.info(f"Executing dummy background task with message: {message}")
    return f"Processed: {message}"
