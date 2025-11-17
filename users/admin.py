from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная админ-панель для модели пользователя.

    Добавляет дополнительные поля в интерфейс администратора Django:
    - Часовой пояс (timezone)
    - Настройки уведомлений (notification_preferences)

    Attributes:
        list_display (tuple): Поля, отображаемые в списке пользователей.
        list_filter (tuple): Фильтры, доступные в боковой панели.
        search_fields (tuple): Поля, по которым возможен поиск.
        ordering (tuple): Порядок сортировки записей в списке.
        fieldsets (tuple): Определение групп полей при редактировании пользователя.
        add_fieldsets (tuple): Определение групп полей при создании нового пользователя.
    """

    list_display = ('username', 'email', 'timezone', 'notification_preferences', 'is_active', 'is_staff')

    list_filter = ('timezone', 'notification_preferences', 'is_active', 'is_staff', 'is_superuser')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Уведомления", {
            "fields": ("timezone", "notification_preferences")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Уведомления", {
            "fields": ("timezone", "notification_preferences"),
        }),
    )