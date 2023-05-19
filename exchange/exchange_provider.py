import abc
import dataclasses
import enum

import requests


class ExchangeCodes(enum.Enum):
    USD = 840
    EUR = 978
    UAH = 980

class ExchangeCodes2(enum.Enum):
    USD = "Dollar"
    EUR = "Euro"
@dataclasses.dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class ExchangeBase(abc.ABC):
    """
    Base class for exchange providers, should define get_rate() method
    """

    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair: SellBuy = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()
        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])

                return


class PrivatExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["ccy"] == self.currency_a and rate["base_ccy"] == self.currency_b:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class MinfinExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.minfin.com.ua/mb/80c6145062cc15795e780fcfe5fe4d41b3c570cc/"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["currency"] == self.currency_a.lower():
                self.pair = SellBuy(float(rate["bid"]), float(rate["ask"]))


class BankGovExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["cc"] == self.currency_a:
                self.pair = SellBuy(float(rate["rate"]), float(rate["rate"]))


class VkurseExchange(ExchangeBase):

    def get_rate(self):

        r = requests.get("https://vkurse.dp.ua/course.json").json()

        for rate in r:
            if rate=="Dollar":
                self.currency_a="USD"
                d_buy =float(r["Dollar"]["buy"])
                d_sale=float(r["Dollar"]["sale"])
                self.pair = SellBuy(d_buy, d_sale)
            elif rate=="Euro":
                self.currency_a = "EUR"
                e_buy = float(r["Dollar"]["buy"])
                e_sale = float(r["Dollar"]["sale"])
                self.pair = SellBuy(e_buy, e_sale)


