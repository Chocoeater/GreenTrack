from django.db import models

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