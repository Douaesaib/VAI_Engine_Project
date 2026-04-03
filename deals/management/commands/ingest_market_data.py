from django.core.management.base import BaseCommand
from deals.models import MarketSignal

class Command(BaseCommand):
    help = 'Ingests initial Layer I market and geopolitical signals into the VAI Engine database.'

    def handle(self, *args, **kwargs):
        signals_data = [
            {'indicator_name': 'Brent Crude Oil (Front Month)', 'category': 'COMMODITY', 'raw_value': 109.41, 'unit': '$/bbl', 'half_life_days': 14},
            {'indicator_name': 'COMEX Copper', 'category': 'COMMODITY', 'raw_value': 5.52, 'unit': '$/lb', 'half_life_days': 14},
            {'indicator_name': 'COMEX Silver', 'category': 'COMMODITY', 'raw_value': 71.33, 'unit': '$/oz', 'half_life_days': 14},
            {'indicator_name': 'US 10-Year Treasury Yield', 'category': 'FIXED_INCOME', 'raw_value': 4.38, 'unit': '%', 'half_life_days': None},
            {'indicator_name': 'US 10Y-2Y Spread', 'category': 'FIXED_INCOME', 'raw_value': 52.0, 'unit': 'bps', 'half_life_days': None},
            {'indicator_name': 'ACLED Daily Incident Volume', 'category': 'GEOPOLITICAL', 'raw_value': 550.0, 'unit': 'Incidents/Day', 'half_life_days': 7},
            {'indicator_name': 'Strait of Hormuz Traffic Reduction', 'category': 'GEOPOLITICAL', 'raw_value': 95.0, 'unit': '% Reduction', 'half_life_days': 7}
        ]

        self.stdout.write(self.style.WARNING('Starting Data Ingestion Process...'))

        for data in signals_data:
            signal, created = MarketSignal.objects.update_or_create(
                indicator_name=data['indicator_name'],
                defaults={
                    'category': data['category'],
                    'raw_value': data['raw_value'],
                    'unit': data['unit'],
                    'half_life_days': data['half_life_days']
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"[{action}] {signal.indicator_name} -> {signal.raw_value} {signal.unit}"))

        self.stdout.write(self.style.SUCCESS('Layer I Data Ingestion Complete!'))