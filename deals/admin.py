from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_class', 'region', 'final_score', 'status')
    list_filter = ('status', 'asset_class')
    search_fields = ('name', 'region')
