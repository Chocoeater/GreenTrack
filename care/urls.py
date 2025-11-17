from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareTypeViewSet, CareTaskViewSet
from care.apps import CareConfig

app_name = CareConfig.name

router = DefaultRouter()
router.register(r'care-types', CareTypeViewSet, basename='care-types')
router.register(r"tasks", CareTaskViewSet, basename="tasks")

urlpatterns = [
    path('', include(router.urls)),
]