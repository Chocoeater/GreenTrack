from django.db import models

from care.models import CareTask


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
    