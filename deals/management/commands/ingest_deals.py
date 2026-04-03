from django.core.management.base import BaseCommand
from deals.models import Deal

class Command(BaseCommand):
    help = 'Ingests the Deal Origination Briefs into the database and auto-calculates scores.'

    def handle(self, *args, **kwargs):
        deals_data = [
            {'name': 'NA BTM Data Centers', 'asset_class': 'PE Infra', 'region': 'North America', 'g': 0.75, 'e': 0.95, 'v': 0.85},
            {'name': 'GCC Bypass Pipelines', 'asset_class': 'PE Infra', 'region': 'GCC', 'g': 0.95, 'e': 0.90, 'v': 0.70},
            {'name': 'Digital Structured Credit', 'asset_class': 'Private Debt', 'region': 'Western Europe', 'g': 0.60, 'e': 0.85, 'v': 0.90},
            {'name': 'Macro Cmdty Arbitrage', 'asset_class': 'Hedge Fund', 'region': 'Global / EM', 'g': 0.95, 'e': 0.85, 'v': 0.95},
            {'name': 'Syrian Rail Corridor', 'asset_class': 'PE Infra', 'region': 'Syria', 'g': 0.90, 'e': 0.90, 'v': 0.90}, 
        ]

        self.stdout.write(self.style.WARNING('Evaluating and Ingesting Deals...'))

        for d in deals_data:
            deal, created = Deal.objects.update_or_create(
                name=d['name'],
                defaults={
                    'asset_class': d['asset_class'],
                    'region': d['region'],
                    'g_score': d['g'],
                    'e_score': d['e'],
                    'v_score': d['v']
                }
            )
            deal.save()
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"[{action}] {deal.name} | Score: {deal.final_score} | Status: {deal.status}"))

        self.stdout.write(self.style.SUCCESS('Deal Ingestion and Scoring Complete!'))