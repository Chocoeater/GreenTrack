from django.contrib import admin

from care.models import CareType, CareTask, CareTaskLog



@admin.register(CareType)
class CareTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_default",
        "order"
    )
    list_filter = (
        "is_default",
        "order"
    )
    search_fields = (
        "name",
        "description"
    )
    ordering = ("order", "name")

    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Дополнительно", {
            "fields": ("is_default", "order"),
            "classes": ("collapse", )
        })
    )

@admin.register(CareTask)
class CareTaskAdmin(admin.ModelAdmin):
    list_display = ('plant', 'care_type', 'last_done', 'next_due', 'frequency_days', 'is_active')
    list_filter = ('is_active', 'care_type', 'next_due', 'last_done')
    search_fields = ('plant__name', 'care_type__name', 'plant__species')
    autocomplete_fields = ['plant']
    readonly_fields = ('next_due',)
    ordering = ('-next_due',)

    fieldsets = (
        (None, {
            'fields': ('plant', 'care_type', 'frequency_days', 'is_active')
        }),
        ('Даты', {
            'fields': ('last_done', 'next_due'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('plant', 'care_type')

@admin.register(CareTaskLog)
class CareTaskLogAdmin(admin.ModelAdmin):
    list_display = ('care_task', 'performed_at', 'notes_preview')
    readonly_fields = ('care_task', 'performed_at', 'notes')
    ordering = ['-performed_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def notes_preview(self, obj):
        return obj.notes[:50] + "..." if len(obj.notes) > 50 else obj.notes
    notes_preview.short_description = "Заметки"