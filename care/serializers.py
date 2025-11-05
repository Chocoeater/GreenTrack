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
    
    Fields:
        id (int): Уникальный идентификатор задачи по уходу.
        plant (int): Ссылка на растение, для которого создана задача.
        care_type (int): Тип ухода (полив, подкормка и т.д.).
        last_done (date): Дата последнего выполнения задачи.
        next_due (date): Дата следующего предполагаемого выполнения (только для чтения).
        is_active (bool): Активна ли задача.
        frequency_days (int): Периодичность выполнения задачи в днях.
    
    Read-only Fields:
        next_due: Вычисляется автоматически на основе last_done и frequency_days.
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
        read_only_fields = ['next_due']