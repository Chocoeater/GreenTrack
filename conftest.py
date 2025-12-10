import pytest
from django.contrib.auth import get_user_model

from care.models import CareTask, CareType
from plants.models import Plant

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="test@example.com",
        timezone="UTC",
        notification_preferences="email",
    )

@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client

@pytest.fixture
def plant(user):
    return Plant.objects.create(
        name="Тестовое растение",
        species="Тестовая растительность",
        image="test.jpg",
        notes="Тестовые заметки",
        created_at="2024-01-01",
        user=user
    )


@pytest.fixture
def care_type():
    return CareType.objects.create(
        name="Тестовый полив",
        description="Поливаем тестом",
        is_default=True,
        order=1,
    )

@pytest.fixture
def care_task(plant, care_type):
    return CareTask.objects.create(
        plant=plant,
        care_type=care_type,
        is_active=True,
        last_done=None,
        next_due=None,
        frequency_days=1,
    )