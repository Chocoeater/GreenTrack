from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

NOTIFICATION_CHOICES = [("email", "Email"),
                        ("bot", "Бот"),
                        ('both', "Email и Бот"),
                        ('none', "Не беспокоить")]

class User(AbstractUser):
    """
    Расширенная модель пользователя, наследующая AbstractUser.

    Добавляет поля для настройки часового пояса и предпочтений уведомлений.

    Attributes:
        timezone (CharField): Часовой пояс пользователя. Используется для корректного
            отображения и отправки напоминаний. По умолчанию — UTC.
        notification_preferences (CharField): Предпочтительный способ получения
            уведомлений. По умолчанию — 'email'.
    """

    timezone = models.CharField(
        max_length=50,
        default="UTC",
        choices=TIMEZONE_CHOICES,
        verbose_name="Часовой пояс",
        help_text="Часовой пояс пользователя, используется для напоминаний",
        blank=True
    )
    notification_preferences = models.CharField(
        max_length=10,
        choices=NOTIFICATION_CHOICES,
        default="email",
        verbose_name="Способ получения уведомлений",
        blank=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def __str__(self):
        """
        Возвращает строковое представление объекта пользователя.

        Returns:
            str: Имя пользователя (username).
        """
        return self.username