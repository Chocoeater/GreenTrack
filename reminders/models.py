from django.db import models
from care.models import CareType
from plants.models import Plant


class CareTask(models.Model):
    """
    Модель для отслеживания задач по уходу за растениями.

    Attributes:
        plant (Plant): Растение, для которого назначена задача по уходу.
                       Связь с моделью Plant через внешний ключ. При удалении
                       растения, все связанные задачи также удаляются.
        care_task (CareType): Тип ухода (например, полив, удобрение).
                              Связь с моделью CareType через внешний ключ.
                              При удалении типа ухода, связанные задачи удаляются.
        last_done (datetime): Дата и время последнего выполнения задачи.
                             Может быть пустым, если задача ещё не выполнялась.
        next_due (datetime): Дата и время следующего запланированного выполнения задачи.
                             Может быть пустым, если дата не установлена.
        is_active (bool): Флаг активности задачи. По умолчанию True.
                          Позволяет деактивировать задачу без её удаления.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="Растение", related_name="care_tasks")
    care_type = models.ForeignKey(CareType, on_delete=models.CASCADE, verbose_name="Уход", related_name="care_tasks")
    last_done = models.DateTimeField(verbose_name="Дата и время последнего выполнения", null=True, blank=True)
    next_due = models.DateTimeField(verbose_name="Дата и время следующего выполнения", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    
    class Meta:
        verbose_name = "Уход"
        verbose_name_plural = "Уходы"
    
    def __str__(self):
        """
        Возвращает строковое представление задачи по уходу.

        Returns:
            str: Строка в формате 'Имя растения - Название типа ухода'.
        """
        return f"{self.plant.name} - {self.care_task.name}"

class CareTaskLog(models.Model):
    """
    Модель для журналирования выполнения задач по уходу за растениями.

    Каждая запись в журнале фиксирует факт выполнения определённой задачи по уходу
    (например, полив, опрыскивание) в определённое время, а также может содержать
    дополнительные заметки о выполнении.

    Attributes:
        care_task (CareTask): Ссылка на задачу по уходу, которая была выполнена.
                              При удалении задачи все связанные записи в журнале
                              также удаляются. Отображается как 'Задача по уходу'.
        performed_at (datetime): Дата и время выполнения задачи. Устанавливается
                                 автоматически при создании записи (auto_now_add=True).
                                 Отображается как 'Дата и время выполнения'.
        notes (str): Дополнительные заметки, которые пользователь может добавить
                     при выполнении задачи. Поле необязательное. Отображается как 'Заметки'.
    """

    care_task = models.ForeignKey(CareTask, on_delete=models.CASCADE, related_name="logs", verbose_name="Задача по уходу")
    performed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время выполнения")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    
    class Meta:
        verbose_name = "Журнал выполнения ухода"
        verbose_name_plural = "Журналы выполнения уходов"
        ordering = ['-performed_at']
        
    def __str__(self):
        """
        Возвращает строковое представление записи в журнале.

        Returns:
            str: Строка в формате 'Имя растения - Название ухода - Дата и время выполнения'.
        """
        return f"{self.care_task} - {self.performed_at}"
    