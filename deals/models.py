from django.db import models

class Deal(models.Model):
    """
    Model representing an investment opportunity processed by the VAI Engine.
    """
    class StatusChoices(models.TextChoices):
        ACTION = 'ACTION', 'Action (Tier 1)'
        SUPPRESS = 'SUPPRESS', 'Suppress (OFAC)'
        MONITOR = 'MONITOR', 'Monitor'

    name = models.CharField(max_length=255, verbose_name="Target Opportunity")
    asset_class = models.CharField(max_length=100, verbose_name="Asset Class")
    region = models.CharField(max_length=150, verbose_name="Geographic Node")
    
    # Scoring variables
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

    def __str__(self):
        return f"{self.name} ({self.asset_class})"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to auto-calculate the final score 
        and apply OFAC jurisdictional gating (sanctions compliance).
        """
        # 1. Jurisdictional Gating: Check for OFAC/FCA sanctioned regions
        sanctioned_keywords = ['syria', 'syrian', 'iran', 'iranian', 'russia', 'russian']
        
        # Check if any sanctioned keyword exists in the region or deal name
        is_sanctioned = any(
            keyword in (self.region.lower() + " " + self.name.lower()) 
            for keyword in sanctioned_keywords
        )

        if is_sanctioned:
            # Auto-suppress opportunities violating sanctions directives
            self.final_score = 0.000
            self.status = self.StatusChoices.SUPPRESS
        else:
            # 2. Calculate Final Score: O = w1(G) + w2(E) + w3(V)
            if self.g_score is not None and self.e_score is not None and self.v_score is not None:
                calculated_score = (self.g_score + self.e_score + self.v_score) / 3.0
                self.final_score = round(calculated_score, 3)
                
                # 3. Apply Tier 1 Action threshold (score >= 0.75)
                if self.final_score >= 0.75:
                    self.status = self.StatusChoices.ACTION
                else:
                    self.status = self.StatusChoices.MONITOR
                    
        # Call the parent class's save method to execute the DB transaction
        super().save(*args, **kwargs)