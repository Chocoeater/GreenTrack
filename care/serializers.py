from rest_framework import serializers

from care.models import CareType, CareTask


class CareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareType
        fields = '__all__'

class CareTaskSerializer(serializers.ModelSerializer):
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