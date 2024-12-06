from django.shortcuts import render
from calculator_app.models import Calculator
# Create your views here.


def calculators(request, *args, **kwargs):
    if request.method == "POST":
        expression = request.POST["expression"]
        result = request.POST["result"]
        c = Calculator()
        c.expression = expression
        c.result = int(result)
        c.save()
    equations = Calculator.objects.all()
    return render(request, "calculator.html", {
        "equations": equations
    })