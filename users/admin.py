from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('username', 'email', 'timezone', 'notification_preferences', 'is_active', 'is_staff')

    # Фильтры справа
    list_filter = ('timezone', 'notification_preferences', 'is_active', 'is_staff', 'is_superuser')

    # Поля для поиска
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Порядок сортировки
    ordering = ('username',)

    # Группировка полей при редактировании
    fieldsets = UserAdmin.fieldsets + (
        ("Уведомления", {
            "fields": ("timezone", "notification_preferences")
        }),
    )

    # Группировка полей при создании
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Уведомления", {
            "fields": ("timezone", "notification_preferences"),
        }),
    )
