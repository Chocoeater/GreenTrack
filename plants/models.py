from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Plant(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя растения', help_text='Введите имя растения')
    species = models.CharField(max_length=200, verbose_name='Вид растения', help_text='Введите вид растения')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение растения', help_text='Загрузите изображение растения')
    notes = models.TextField(verbose_name='Заметки', help_text='Введите заметки о растении', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'
        ordering = ['-created_at']
