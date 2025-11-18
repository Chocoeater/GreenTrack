from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from plants.models import Plant
from plants.serializers import PlantSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список растений",
        description="Возвращает список растений пользователя. ",
    ),
    retrieve=extend_schema(
        summary="Детали растения", description="Возвращает полную информацию о растении."
    ),
    create=extend_schema(
        summary="Создание растения",
        description="Создает новое растение для текущего пользователя.",
    ),
    update=extend_schema(
        summary="Обновление растения",
        description="Полное обновление растения.",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление растения",
        description="Частичное обновление растения.",
    ),
    destroy=extend_schema(
        summary="Удаление растения",
        description="Удаляет растение.",
    ),
)
class PlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления растениями.

    Предоставляет операции CRUD для модели Plant.
    Доступ к растениям ограничен пользователем: пользователь может видеть и управлять только своими растениями.
    """
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]
    queryset = Plant.objects.all() # Для spectacular

    def get_queryset(self):
        """
        Возвращает queryset растений, принадлежащих текущему пользователю.

        Используется для фильтрации объектов при GET-запросах (список и детали).
        """
        return Plant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Выполняется при создании нового растения.

        Присваивает текущего пользователя как владельца растения.

        Args:
            serializer (PlantSerializer): Сериализатор с валидированными данными.
        """
        serializer.save(user=self.request.user)