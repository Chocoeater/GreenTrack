from rest_framework import serializers

from plants.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Plant.

    Предоставляет сериализацию и десериализацию данных для объектов Plant.
    Включает проверку обязательных полей и настройки только для чтения.

    Поля:
        id (int): Уникальный идентификатор растения (только для чтения).
        name (str): Название растения. Обязательное поле.
        species (str): Вид растения. Обязательное поле.
        image (Image): Изображение растения. Необязательное поле.
        notes (str): Дополнительные заметки о растении.
        created_at (datetime): Дата и время создания записи (только для чтения).

    Атрибуты:
        read_only_fields (list): Поля, доступные только для чтения.
        extra_kwargs (dict): Дополнительные аргументы для полей, например, указание обязательности.
    """
    class Meta:
        model = Plant
        fields = [
            'id',
            'name',
            'species',
            'image',
            'notes',
            'created_at'
            ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'name': {'required': True},
            'species': {'required': True},
            'image': {'required': False},
        }