import json
import pathlib

import responses

from .exchange_provider import (
    MonoExchange,
    PrivatExchange,
    MinfinExchange,
    BankGovExchange,
    VkurseExchange,
)

root = pathlib.Path(__file__).parent

# Create your tests here.


@responses.activate
def test_exchange_mono():
    mocked_response = json.load(open(root / "fixtures/mono_response.json"))
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406


def test_privat_rate():
    mocked_response = json.load(open(root / "fixtures/privat_response.json"))
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.45318


def test_minfin_rate():
    mocked_response = json.load(open(root / "fixtures/minfin_response.json"))
    responses.get(
        "https://api.minfin.com.ua/mb/80c6145062cc15795e780fcfe5fe4d41b3c570cc/",
        json=mocked_response,
    )
    e = MinfinExchange("minfin", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686


def test_bank_gov_rate():
    mocked_response = json.load(open(root / "fixtures/bank_gov_response.json"))
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json/",
        json=mocked_response,
    )
    e = BankGovExchange("bank_gov", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686


def test_currency_rate():
    mocked_response = json.load(open(root / "fixtures/vkurse_response.json"))
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4
