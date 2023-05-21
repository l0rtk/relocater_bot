import requests

def get_currencies(date):
    req = requests.get(f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date={date}")
    return req.json()


def get_currency(date,currency = "USD"):
    req = requests.get(f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?currencies={currency}&date={date}")
    return req.json()

from pprint import pprint
from datetime import datetime


pprint(get_currency(datetime(2023,4,16), "EUR"))