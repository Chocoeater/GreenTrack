from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care import serializers
from care.models import CareType, CareTask
from care.services import mark_task_as_done


class CareTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели CareType.

    Предоставляет только чтение (list, retrieve) типов ухода,
    доступных по умолчанию (is_default=True).
    Доступ разрешён только аутентифицированным пользователям.
    """

    queryset = CareType.objects.filter(is_default=True)
    serializer_class = serializers.CareTypeSerializer
    permission_classes = [IsAuthenticated]


class CareTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления задачами по уходу за растениями.

    Позволяет просматривать, создавать, обновлять, удалять и отмечать
    выполненные задачи. Доступ к задачам ограничен пользователем — владеющим растением.
    """

    serializer_class = serializers.CareTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает queryset задач, связанных с растениями текущего пользователя.

        Используется select_related для оптимизации запросов к полям 'plant' и 'care_type'.
        """
        return CareTask.objects.filter(plant__user=self.request.user).select_related('plant', 'care_type')

    def perform_create(self, serializer):
        """
        Выполняет дополнительную проверку при создании задачи.

        Убеждается, что растение принадлежит текущему пользователю.
        В случае нарушения — выбрасывает ValidationError.

        Args:
            serializer (serializers.CareTaskSerializer): Сериализатор с валидированными данными.
        """
        plant = serializer.validated_data['plant']
        if plant.user != self.request.user:
            raise ValidationError("Вы не можете создать задачу для чужого растения")
        serializer.save()

    @action(detail=True, methods=['post'], url_path='done')
    def mark_as_done(self, request, pk=None):
        """
        Действие для отметки задачи как выполненной.

        При вызове обновляет статус задачи, сохраняет заметки и вычисляет следующую дату выполнения.
        В случае ошибки возвращается 400, при успехе — 200 с информацией о следующем сроке.

        Args:
            request (Request): HTTP-запрос с опциональными 'notes'.
            pk (int): Первичный ключ задачи.

        Returns:
            Response: JSON с сообщением и датой следующего выполнения или ошибкой.
        """
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
