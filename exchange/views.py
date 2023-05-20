import datetime
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render

from .forms import CalculationForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


# Create your views here.


def index(request):
    current_date = datetime.date.today()
    form = CalculationForm(request.POST)
    if request.method == "POST" and form.is_valid():
        if "USD-UAH" in request.POST:
            num = form.cleaned_data["num"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="USD")
                .all()
                .values()
                .order_by("buy")
            )
            cof = list(current_rates)[-1]["buy"]
            vendor = list(current_rates)[-1]["vendor"]
            result = num * float(cof)
            return JsonResponse({vendor: result}, encoder=DecimalAsFloatJSONEncoder)
        elif "EUR-UAH" in request.POST:
            num = form.cleaned_data["num"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="EUR")
                .all()
                .values()
                .order_by("buy")
            )
            cof = list(current_rates)[-1]["buy"]
            vendor = list(current_rates)[-1]["vendor"]
            result = num * float(cof)
            return JsonResponse({vendor: result}, encoder=DecimalAsFloatJSONEncoder)
        elif "UAH-USD" in request.POST:
            num = form.cleaned_data["num"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="USD")
                .all()
                .values()
                .order_by("sell")
            )
            cof = list(current_rates)[0]["sell"]
            vendor = list(current_rates)[0]["vendor"]
            result = num * 1 / float(cof)
            return JsonResponse({vendor: result}, encoder=DecimalAsFloatJSONEncoder)
        elif "UAH-EUR" in request.POST:
            num = form.cleaned_data["num"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="EUR")
                .all()
                .values()
                .order_by("sell")
            )
            cof = list(current_rates)[0]["sell"]
            vendor = list(current_rates)[0]["vendor"]
            result = num * 1 / float(cof)
            return JsonResponse({vendor: result}, encoder=DecimalAsFloatJSONEncoder)
    else:
        form = CalculationForm()
        return render(request, "choice.html", {"form": form})
