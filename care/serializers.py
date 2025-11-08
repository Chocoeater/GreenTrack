from rest_framework import serializers

from care.models import CareType, CareTask


class CareTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CareType.
    
    Преобразует объекты модели CareType в JSON-представление и обратно.
    Включает все поля модели.
    
    Поля:
        Все поля модели CareType.
    """

    class Meta:
        model = CareType
        fields = '__all__'


class CareTaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CareTask.

    Преобразует объекты модели CareTask в JSON-представление и обратно.
    Поддерживает валидацию полей и вычисление автоматических значений.

    Поля:
        id (int): Уникальный идентификатор задачи по уходу. Автоматически генерируется при создании.
        plant (int): Ссылка на растение (внешний ключ), для которого создана задача. Обязательное поле.
        care_type (int): Тип ухода (например, полив, подкормка). Ссылка на модель CareType. Обязательное поле.
        last_done (date): Дата последнего выполнения задачи. Используется для расчёта следующего срока.
        next_due (date): Ожидаемая дата следующего выполнения задачи. Поле только для чтения, вычисляется автоматически.
        is_active (bool): Флаг активности задачи. Если False — задача временно отключена.
        frequency_days (int): Периодичность выполнения задачи в днях. Определяет интервал между уходами.

    Дополнительные настройки (extra_kwargs):
        - 'plant': обязательное поле.
        - 'care_type': обязательное поле.
        - 'next_due': обязательное поле, в дальнейшем будет вычисляться автоматически.
    """

    class Meta:
        model = CareTask
        fields = [
            'id',
            'plant',
            'care_type',
            'last_done',
            'next_due',
            'is_active',
            'frequency_days'
        ]
        
        extra_kwargs = {
            'plant': {'required': True},
            'care_type': {'required': True},
            'next_due': {'required': True},
        }