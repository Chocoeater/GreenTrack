from datetime import date, timedelta

from rest_framework.exceptions import ValidationError

from care.models import CareTask, CareTaskLog



def mark_task_as_done(task: CareTask, notes: str = "") -> CareTask:
    today = date.today()

    if not task.is_active:
        raise ValidationError("Нельзя выполнить неактивную задачу")

    if task.last_done == today:
        raise ValidationError("Задача уже выполнена сегодня")

    task.last_done = today
    task.save(update_fields=["last_done"])

    task.update_next_due()

    CareTaskLog.objects.create(
        care_task=task, notes=notes
    )

    return task