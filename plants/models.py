from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

def plant_image_upload_to(instance, filename):
    """
    Динамически генерирует путь для загрузки изображения растения.

    Args:
        instance (Plant): Экземпляр модели Plant
        filename (str): Оригинальное имя файла

    Returns:
        str: Путь вида 'images/plants/user_1/photo.jpg'
    """
    return f'images/plants/user_{instance.user.id}/{filename}'

class Plant(models.Model):
    """
    Модель для представления растения в системе.

    Attributes:
        name (CharField): Название растения. Ограничено 200 символами.
        species (CharField): Вид растения. Ограничено 200 символами.
        image (ImageField): Изображение растения, загружаемое в папку 'images/'.
        notes (TextField): Дополнительные заметки о растении. Поле необязательное.
        created_at (DateTimeField): Дата и время создания записи. Автоматически устанавливается при создании.
        user (ForeignKey): Связь с пользователем, который добавил растение. При удалении пользователя,
                          все его растения также удаляются.
    """

    name = models.CharField(max_length=200, verbose_name='Имя растения', help_text='Введите имя растения')
    species = models.CharField(max_length=200, verbose_name='Вид растения', help_text='Введите вид растения')
    image = models.ImageField(upload_to=plant_image_upload_to, verbose_name='Изображение растения', help_text='Загрузите изображение растения', null=True, blank=True)
    notes = models.TextField(verbose_name='Заметки', help_text='Введите заметки о растении', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')

    def __str__(self):
        """
        Возвращает строковое представление растения (его имя).

        Returns:
            str: Имя растения.
        """
        return self.name

    class Meta:
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'
        ordering = ['-created_at']
