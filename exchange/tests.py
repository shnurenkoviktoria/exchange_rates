import json
import pathlib

import pytest
import responses
from django.core.management import call_command
from django.test import RequestFactory
from django.urls import reverse
from freezegun import freeze_time

from . import views
from .exchange_provider import (
    MonoExchange,
    PrivatExchange,
    MinfinExchange,
    BankGovExchange,
    VkurseExchange,
)

root = pathlib.Path(__file__).parent


# Create your tests here.
@pytest.fixture
def mocked():
    def inner(file_name):
        return json.load(open(root / "fixtures" / file_name))

    return inner


@responses.activate
def test_exchange_mono(mocked):
    mocked_response = mocked("mono_response.json")
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406


@responses.activate
def test_privat_rate(mocked):
    mocked_response = mocked("privat_response.json")
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.45318


@responses.activate
def test_minfin_rate(mocked):
    mocked_response = mocked("minfin_response.json")
    responses.get(
        "https://api.minfin.com.ua/mb/80c6145062cc15795e780fcfe5fe4d41b3c570cc/",
        json=mocked_response,
    )
    e = MinfinExchange("minfin", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686


@responses.activate
def test_bank_gov_rate(mocked):
    mocked_response = mocked("bank_gov_response.json")
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json/",
        json=mocked_response,
    )
    e = BankGovExchange("bank_gov", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686


def test_vkurse_rate(mocked):
    mocked_response = mocked("vkurse_response.json")
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.0


@pytest.fixture
def rf():
    return RequestFactory()


@responses.activate
def test_index_view(rf):
    url = reverse("index")
    request = rf.post(url, data={"USD-UAH": ""})
    response = views.index(request)
    assert response.status_code == 302

    request = rf.post(url, data={"EUR-UAH": ""})
    response = views.index(request)
    assert response.status_code == 302

    request = rf.post(url, data={"UAH-USD": ""})
    response = views.index(request)
    assert response.status_code == 302

    request = rf.post(url, data={"UAH-EUR": ""})
    response = views.index(request)
    assert response.status_code == 302

    request = rf.get(url)
    response = views.index(request)
    assert response.status_code == 200


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "db_init.yaml")


@freeze_time("2022-01-01")
@pytest.mark.django_db
def test_exchange_rate_post_view(rf):
    url = reverse("usd-uah")
    request = rf.post(url, {"num": 1})
    response = views.usd_uah(request)
    assert json.loads(response.content) == {"minfin": 1.6}

    request = rf.get(url)
    response = views.usd_uah(request)
    assert response.status_code == 200


@freeze_time("2022-01-01")
@pytest.mark.django_db
def test_1exchange_rate_post_view(rf):
    url = reverse("uah-usd")
    request = rf.post(url, {"num": "1"})
    response = views.uah_usd(request)
    assert json.loads(response.content) == {"mono": 0.9090909090909091}

    request = rf.get(url)
    response = views.uah_usd(request)
    assert response.status_code == 200


@freeze_time("2022-01-01")
@pytest.mark.django_db
def test_2exchange_rate_post_view(rf):
    url = reverse("eur-uah")
    request = rf.post(url, {"num": 1})
    response = views.eur_uah(request)
    assert json.loads(response.content) == {"bank_gov": 2.8}

    request = rf.get(url)
    response = views.eur_uah(request)
    assert response.status_code == 200


@freeze_time("2022-01-01")
@pytest.mark.django_db
def test_3exchange_rate_post_view(rf):
    url = reverse("uah-eur")
    request = rf.post(url, {"num": "1"})
    response = views.uah_eur(request)
    assert json.loads(response.content) == {"mono": 0.47619047619047616}

    request = rf.get(url)
    response = views.uah_eur(request)
    assert response.status_code == 200
