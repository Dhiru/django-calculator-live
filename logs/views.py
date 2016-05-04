import urllib


from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Calculator, Log


def index(request):
    """
    Root page view. Just shows a list of calculators.
    """
    # Get a list of calculator, ordered by the date of their most recent
    # log, descending (so ones with stuff happening are at the top)
    calculators = Calculator.objects.annotate(
        max_created=Max("logs__created")
    ).order_by("-max_created")

    # Render that in the index template
    return render(request, "index.html", {
        "calculators": calculators,
    })


def calculator(request, slug):
    """
    Shows an individual calculator page.
    """
    # Get the calculator by slug
    calculator = get_object_or_404(Calculator, slug=slug)

    # Render it with the logs ordered in descending order.
    # If the user has JavaScript enabled, the template has JS that will
    # keep it updated.
    return render(request, "calculator.html", {
        "calculator": calculator,
        "logs": calculator.logs.order_by("-created"),
    })

def log(request, calculator_slug, log_body):
    """
    Log a calculation on a particular calculator
    """
    print calculator_slug, log_body
    calculator = get_object_or_404(Calculator, slug=calculator_slug)

    if calculator:
        log = Log(calculator=calculator, body=log_body)
        log.save()
        print log

    # Render the 201 created template
    return render(request, "201.html")
