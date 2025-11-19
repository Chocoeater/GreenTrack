from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care import serializers
from care.models import CareType, CareTask
from care.services import mark_task_as_done

@extend_schema_view(
    list=extend_schema(
        summary="Список типов ухода",
        description="Возвращает список типов ухода по умолчанию.",
    ),
    retrieve=extend_schema(
        summary="Детали типа ухода",
        description="Возвращает полную информацию о типе ухода.",
    )
)
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

@extend_schema_view(
    list=extend_schema(
        summary="Список задач по уходу",
        description="Возвращает список задач по уходу за растениями текущего пользователя.",
    ),
    retrieve=extend_schema(
        summary="Детали задачи по уходу",
        description="Возвращает полную информацию о задаче по уходу.",
    ),
    create=extend_schema(
        summary="Создание задачи по уходу",
        description="Создает новую задачу по уходу за растением пользователя.",
    ),
    update=extend_schema(
        summary="Обновление задачи по уходу",
        description="Полное обновление информации о задаче по уходу.",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление задачи по уходу",
        description="Частичное обновление информации о задаче по уходу.",
    ),
    destroy=extend_schema(
        summary="Удаление задачи по уходу",
        description="Удаляет задачу по уходу за растением.",
    ),
)
class CareTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления задачами по уходу за растениями.

    Позволяет просматривать, создавать, обновлять, удалять и отмечать
    выполненные задачи. Доступ к задачам ограничен пользователем — владеющим растением.
    """

    serializer_class = serializers.CareTaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = CareTask.objects.all()  # Для spectacular

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

    @extend_schema(
        summary="Отметить задачу как выполненную",
        description="Отмечает задачу по уходу как выполненную и вычисляет следующую дату выполнения.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'notes': {'type': 'string', 'description': 'Заметки к выполненной задаче', 'required': False}
                }
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string', 'example': 'Задача отмечена как выполненная'},
                    'next_due': {'type': 'string', 'format': 'date-time', 'example': '2024-01-15T10:00:00Z'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Текст ошибки валидации'}
                }
            }
        },
        examples=[
            OpenApiExample(
                'Пример успешного запроса',
                summary='Запрос с заметками',
                value={'notes': 'Полил растение утром'},
                request_only=True
            ),
            OpenApiExample(
                'Пример успешного ответа',
                summary='Успешное выполнение',
                value={
                    'detail': 'Задача отмечена как выполненная',
                    'next_due': '2024-01-17T10:00:00Z'
                },
                response_only=True,
                status_codes=['200']
            ),
            OpenApiExample(
                'Пример ошибки',
                summary='Ошибка валидации',
                value={
                    'error': 'Нельзя отметить задачу как выполненную до наступления срока'
                },
                response_only=True,
                status_codes=['400']
            ),
        ]
    )
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
