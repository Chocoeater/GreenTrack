from datetime import date, timedelta

from rest_framework.exceptions import ValidationError

from care.models import CareTask, CareTaskLog



def mark_task_as_done(task: CareTask, notes: str = "") -> CareTask:
    """
    Отмечает задачу по уходу как выполненную на текущий день.

    Проверяет, активна ли задача, и не была ли она уже выполнена сегодня.
    Обновляет дату последнего выполнения, рассчитывает следующую дату выполнения
    и создает запись в логе выполнения задачи.

    Args:
        task (CareTask): Экземпляр задачи по уходу, которую нужно отметить как выполненную.
        notes (str, optional): Дополнительные заметки к выполнению задачи. По умолчанию "".

    Returns:
        CareTask: Обновлённый экземпляр задачи.

    Raises:
        ValidationError: Если задача неактивна или уже была выполнена сегодня.
    """
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