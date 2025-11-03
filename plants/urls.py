from django.urls import path, include
from rest_framework.routers import DefaultRouter
from plants import views
from plants.apps import PlantsConfig

app_name = PlantsConfig.name

router = DefaultRouter()
router.register(r'plants', views.PlantViewSet, basename='plants')

urlpatterns = [
    path('', include(router.urls)),
]