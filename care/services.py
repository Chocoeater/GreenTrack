from datetime import date, timedelta

from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from care.models import CareTask, CareTaskLog
from tracker import settings
from users.models import User



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

def send_daily_care(user: User, due_tasks: list[CareTask]) -> bool:
    if not due_tasks:
        return False

    subject = "Ежедневное напоминание о уходе"

    plant_tasks = []
    for task in due_tasks:
        plant_tasks.append(f"- {task.care_type.name} для {task.plant.name}")

    plant_list = "\n".join(plant_tasks)

    message = (
        f"Привет, {user.first_name or user.username}!\n\n"
        f"Сегодня тебе нужно позаботиться о своих зеленых питомцах:\n\n"
        f"{plant_list}\n\n"
        f"Не забудь проверить и отметь выполнение задач по уходу!"
    )

    print('ОТПРАВКА СООБЩЕНИЯ: ' + '\n' + message)
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки сводного напоминания для {user.email}: {e}")
        return False