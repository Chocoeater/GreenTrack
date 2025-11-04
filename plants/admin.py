from django.contrib import admin

from plants.models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'user', 'created_at')
    list_filter = ('created_at', 'species', 'user')
    search_fields = ('name', 'species', 'user__username', 'user__email')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['user']