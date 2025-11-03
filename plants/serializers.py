from rest_framework import serializers

from plants.models import Plant


class PlantSerializer(serializers.ModelSerializer):
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