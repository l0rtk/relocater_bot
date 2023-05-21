import requests

def get_currencies(date):
    req = requests.get(f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?date={date}")
    return req.json()


def get_currency(date,currency = "USD"):
    currencies = get_currencies(date)
    if currencies:
        for c in currencies[0]['currencies']:
            if c['code'] == currency:
                c["success"] = True
                return c

    return { "success" : False }