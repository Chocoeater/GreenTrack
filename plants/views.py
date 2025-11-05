from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from plants.models import Plant
from plants.serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления растениями.

    Позволяет пользователям просматривать, создавать, редактировать и удалять
    свои собственные растения. Доступ к функционалу доступен только аутентифицированным пользователям.

    Поля:
        serializer_class (PlantSerializer): Сериализатор для модели Plant.
        permission_classes (list): Разрешения доступа — только аутентифицированные пользователи.

    Методы:
        get_queryset(): Возвращает растения, принадлежащие текущему пользователю.
        perform_create(serializer): При создании растения автоматически присваивает его текущему пользователю.
    """
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает QuerySet растений, принадлежащих текущему пользователю.

        Returns:
            QuerySet: Растения, связанные с пользователем из запроса.
        """
        return Plant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Выполняется при создании нового растения.

        Автоматически сохраняет растение, привязывая его к текущему пользователю.

        Args:
            serializer (PlantSerializer): Сериализатор с валидированными данными.
        """
        serializer.save(user=self.request.user)