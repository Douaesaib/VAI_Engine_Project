from django.db import models


class Deal(models.Model):
    
    class StatusChoices(models.TextChoices):
        ACTION = 'ACTION', 'Action (Tier 1)'
        SUPPRESS = 'SUPPRESS', 'Suppress (OFAC)'
        MONITOR = 'MONITOR', 'Monitor'

    name = models.CharField(max_length=255, verbose_name="Target Opportunity")
    asset_class = models.CharField(max_length=100, verbose_name="Asset Class")
    region = models.CharField(max_length=150, verbose_name="Geographic Node")
    
    # empty scores
    g_score = models.FloatField(null=True, blank=True, verbose_name="Geopolitical Score (G)")
    e_score = models.FloatField(null=True, blank=True, verbose_name="Economic Score (E)")
    v_score = models.FloatField(null=True, blank=True, verbose_name="Valuation Score (V)")
    
    final_score = models.FloatField(null=True, blank=True, verbose_name="Final O Score")
    
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.MONITOR,
        verbose_name="Investment Status"
    )

    # showing project with name 
    def __str__(self):
        return f"{self.name} ({self.asset_class})"
