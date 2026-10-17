from clients import rates, weather
from processing import preprocessing


def build_city_summary(city, currency="USD"):
    w = weather.get_weather(city)
    rate = rates.get_rate(currency)

    return {
        "city": city,
        "weather": {
            "temp_c": w["temp_c"],
            "description": preprocessing.strip_description(w.get("description")),
            "warm_clothes": preprocessing.warm_clothes(w["temp_c"]),
        },
        "rates": {
            "currency": currency.upper(),
            "rate_to_rub": rate,
            "expensive": preprocessing.expensive(rate),
        },
    }