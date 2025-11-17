import logging

from celery import shared_task
from django.utils import timezone

from care.models import CareTask
from care.services import send_daily_care

logger = logging.getLogger(__name__)

@shared_task
def check_due_tasks():
    """
    Периодическая задача: проверяет, какие задачи по уходу
    должны быть выполнены сегодня, и отправляет напоминания.
    """

    logger.info("Задача check_due_tasks запущена")
    today = timezone.now().date()
    due_tasks = CareTask.objects.filter(
        next_due=today,
        is_active=True
    ).select_related('plant__user', 'care_type')

    user_tasks = {}
    for task in due_tasks:
        user = task.plant.user
        if user not in user_tasks:
            user_tasks[user] = []
        user_tasks[user].append(task)

    for user, tasks in user_tasks.items():
        send_daily_care(user, tasks)