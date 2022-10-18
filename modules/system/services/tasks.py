from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

from modules.system.services.email import send_activate_email_message

logger = get_task_logger(__name__)


@shared_task
def send_activate_email_task(email):
    """
    1. Получение из view регистрации
    2. Отправка через функцию send_activate_email_message
    """
    return send_activate_email_message(email)


@shared_task()
def db_backup_task():
    """
    Выполнение резервного копирования базы данных
    """
    logger.info('Backup database starting')
    call_command('dbackup',)