from django.contrib import admin
from .models import Deal, MarketSignal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_class', 'region', 'final_score', 'status')
    list_filter = ('status', 'asset_class')
    search_fields = ('name', 'region')
@admin.register(MarketSignal)
class MarketSignalAdmin(admin.ModelAdmin):
    list_display = ('indicator_name', 'category', 'raw_value', 'unit', 'current_decayed_value', 'ingested_at')
    list_filter = ('category',)
