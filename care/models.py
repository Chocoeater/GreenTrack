from datetime import timedelta

from django.db import models

from plants.models import Plant


class CareType(models.Model):
    """
    Модель для представления типа ухода за растением.

    Атрибуты:
        name (CharField): Название типа ухода. Должно быть уникальным.
                         Ограничено 255 символами, не может быть пустым.
        frequency_days (PositiveIntegerField): Периодичность выполнения ухода в днях.
                                               По умолчанию — 1 день.
        description (TextField): Дополнительные рекомендации или описание по уходу.
                                 Поле необязательное, может быть пустым.
        is_default (BooleanField): Флаг, указывающий, является ли этот тип ухода
                                   типом по умолчанию. По умолчанию — False.
        order (PositiveIntegerField): Определяет порядок отображения типов ухода
                                      в интерфейсе. По умолчанию — 0.
    """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name="Тип ухода", help_text="Введите тип ухода")
    frequency_days = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="Частота ухода (в днях)", help_text="Введите частоту ухода в днях (по умолчанию 1 день)")
    description = models.TextField(null=True, blank=True, verbose_name="Описание", help_text="Введите рекомендации по типу ухода")
    is_default = models.BooleanField(default=False, verbose_name="По умолчанию", help_text="Отметьте, если это тип ухода по умолчанию")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок", help_text="Укажите порядок отображения типов ухода")
    
    class Meta:
        verbose_name = "Тип ухода"
        verbose_name_plural = "Типы ухода"
        ordering = ['order']

    def __str__(self):
        """Возвращает название типа ухода."""
        return self.name


class CareTask(models.Model):
    """
    Модель для отслеживания задач по уходу за растениями.

    Представляет конкретную задачу по уходу за растением, привязанную к определённому типу ухода
    и запланированную с учётом периодичности. Автоматически обновляет дату следующего выполнения
    на основе даты последнего выполнения и указанной частоты.

    Атрибуты:
        plant (ForeignKey): Растение, для которого создана задача.
                           При удалении растения, все связанные задачи удаляются.
                           Отображается как 'Растение' в интерфейсе администратора.
        care_type (ForeignKey): Тип ухода (например, полив, опрыскивание, подкормка).
                               Связь с моделью CareType. При удалении типа ухода,
                               связанные задачи также удаляются.
                               Отображается как 'Тип ухода' в интерфейсе.
        last_done (DateField): Дата последнего выполнения задачи. Может быть пустой,
                               если задача ещё не выполнялась. Обновляется вручную или через логику приложения.
        next_due (DateField): Дата следующего предполагаемого выполнения задачи.
                              Вычисляется автоматически на основе last_done и frequency_days.
                              Может быть пустой, если last_done не задан.
        is_active (BooleanField): Определяет, активна ли задача. По умолчанию — True.
                                  Позволяет временно отключить задачу без её удаления.

    Методы:
        __str__: Возвращает строку в формате 'Имя растения - Название типа ухода'.
        update_next_due: Автоматически вычисляет и сохраняет дату следующего выполнения
                         как last_done + frequency_days.

    Мета:
        verbose_name: Отображаемое имя модели — 'Задача по уходу'.
        verbose_name_plural: Отображаемое имя во множественном числе — 'Задачи по уходу'.
        ordering: Задачи упорядочены по дате следующего выполнения (next_due).

    Пример:
        CareTask(plant=орхидея, care_type=полив, last_done='2025-04-01', next_due='2025-04-03')
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="Растение", related_name="care_tasks")
    care_type = models.ForeignKey(CareType, on_delete=models.PROTECT, verbose_name="Тип ухода", related_name="care_tasks")
    last_done = models.DateField(verbose_name="Дата последнего выполнения", null=True, blank=True)
    next_due = models.DateField(verbose_name="Дата следующего выполнения", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активность", default=True)

    class Meta:
        verbose_name = "Задача по уходу"
        verbose_name_plural = "Задачи по уходу"
        ordering = ['is_active', 'next_due']

    def __str__(self):
        """
        Возвращает строковое представление задачи по уходу.

        Returns:
            str: Строка в формате 'Имя растения - Название типа ухода'.
        """
        return f"{self.plant.name} - {self.care_type.name}"
    
    def update_next_due(self):
        """
        Обновляет дату следующего выполнения задачи на основе последнего выполнения
        и установленной частоты ухода.

        Если last_done и frequency_days заданы, next_due устанавливается как
        last_done + frequency_days. Результат сохраняется в базе данных
        с использованием update_fields для оптимизации.

        Примечание:
            Метод вызывает save() с указанием поля 'next_due', чтобы избежать
            лишних операций при обновлении.
        """
        if self.last_done and self.care_type.frequency_days:
            self.next_due = self.last_done + timedelta(days=self.care_type.frequency_days)
            self.save(update_fields=['next_due'])
