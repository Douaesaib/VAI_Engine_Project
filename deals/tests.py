from django.test import TestCase
from .models import Deal

class DealModelTest(TestCase):
    """
    Test suite for the Deal model's business logic, including 
    scoring calculations and OFAC sanction gating.
    """

    def test_calculate_tier1_score(self):
        """
        Test that a deal with high scores correctly calculates the average
        and assigns the 'ACTION' status.
        """
        deal = Deal.objects.create(
            name="NA BTM Data Centers",
            asset_class="PE Infra",
            region="North America",
            g_score=0.75,
            e_score=0.95,
            v_score=0.85
        )
        self.assertEqual(deal.final_score, 0.85)
        self.assertEqual(deal.status, 'ACTION')

    def test_ofac_sanctions_suppress(self):
        """
        Test that a deal in a sanctioned region (e.g., Syria) is automatically
        suppressed with a score of 0.000, regardless of input scores.
        """
        deal = Deal.objects.create(
            name="Syrian Rail Corridor",
            asset_class="PE Infra",
            region="Syria",
            g_score=0.95,
            e_score=0.90,
            v_score=0.90
        )
        self.assertEqual(deal.final_score, 0.0)
        self.assertEqual(deal.status, 'SUPPRESS')

    def test_monitor_status(self):
        """
        Test that a deal with a final score below 0.75 gets the 'MONITOR' status.
        """
        deal = Deal.objects.create(
            name="Average Digital Credit",
            asset_class="Private Debt",
            region="Western Europe",
            g_score=0.50,
            e_score=0.60,
            v_score=0.70
        )
        self.assertEqual(deal.final_score, 0.6)
        self.assertEqual(deal.status, 'MONITOR')
