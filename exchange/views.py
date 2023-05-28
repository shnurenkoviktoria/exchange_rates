import datetime
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CalculationForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


# Create your views here.


def index(request):
    if request.method == "POST":
        if "USD-UAH" in request.POST:
            return HttpResponseRedirect(reverse("usd-uah"))
        elif "EUR-UAH" in request.POST:
            return HttpResponseRedirect(reverse("eur-uah"))
        elif "UAH-USD" in request.POST:
            return HttpResponseRedirect(reverse("uah-usd"))
        elif "UAH-EUR" in request.POST:
            return HttpResponseRedirect(reverse("uah-eur"))
    else:
        return render(request, "choice.html")


def usd_uah(request):
    current_date = datetime.date.today()
    form = CalculationForm(request.POST)
    if request.method == "POST" and form.is_valid():
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

    else:
        form = CalculationForm()
        return render(request, "USD-UAH.html", {"form": form})


def eur_uah(request):
    current_date = datetime.date.today()
    form = CalculationForm(request.POST)
    if request.method == "POST" and form.is_valid():
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
    else:
        form = CalculationForm()
        return render(request, "EUR-UAH.html", {"form": form})


def uah_usd(request):
    current_date = datetime.date.today()
    form = CalculationForm(request.POST)
    if request.method == "POST" and form.is_valid():
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
    else:
        form = CalculationForm()
        return render(request, "UAH-USD.html", {"form": form})


def uah_eur(request):
    current_date = datetime.date.today()
    form = CalculationForm(request.POST)
    if request.method == "POST" and form.is_valid():
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
        return render(request, "UAH-EUR.html", {"form": form})
