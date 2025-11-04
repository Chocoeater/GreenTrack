from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from care import serializers
from care.models import CareType, CareTask
from care.services import mark_task_as_done


class CareTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CareType.objects.filter(is_default=True)
    serializer_class = serializers.CareTypeSerializer
    permission_classes = [IsAuthenticated]

class CareTaskViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CareTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareTask.objects.filter(plant__user=self.request.user).select_related('plant', 'care_type')

    def perform_create(self, serializer):
        plant = serializer.validated_data['plant']
        if plant.user != self.request.user:
            raise serializers.ValidationError("Вы не можете создать задачу для чужого растения")
        serializer.save()

    @action(detail=True, methods=['post'], url_path='done')
    def mark_as_done(self, request, pk=None):
        task = self.get_object()

        notes = request.data.get('notes', '')

        try:
            updated_task = mark_task_as_done(task, notes)
            return Response(
                {
                    'detail': 'Задача отмечена как выполненная', 'next_due': updated_task.next_due,
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
