from django.shortcuts import render
from .models import Deal
from .services import run_monte_carlo_irr_simulation

def dashboard(request):
    """
    Renders the main dashboard displaying all processed investment opportunities.
    Deals are ordered by their final score in descending order.
    """
    # Fetch all deals and order them from highest score to lowest
    deals = Deal.objects.all().order_by('-final_score')
    
    context = {
        'deals': deals,
        'simulation': simulation_results
    }
    return render(request, 'deals/dashboard.html', context)