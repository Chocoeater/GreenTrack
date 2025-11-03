from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from plants.models import Plant
from plants.serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


