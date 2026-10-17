import time
from clients.http import get_json, NotFoundError, BadResponseError

RATE_URL = "https://api.frankfurter.dev/v2/rate/{currency}/RUB"
CACHE_TTL = 300
_cache = {}


def get_rate(currency):
    currency = currency.upper()
    now = time.monotonic()

    if currency in _cache:
        rate, ts = _cache[currency]
        if now - ts < CACHE_TTL:
            return rate

    data = get_json(RATE_URL.format(currency=currency))
    if not isinstance(data, dict):
        raise BadResponseError("rate")

    rate = data.get("rate")
    if rate is None and isinstance(data.get("rates"), dict):
        rate = data["rates"].get("RUB")

    if rate is None:
        raise NotFoundError(f"currency not found: {currency}")

    _cache[currency] = (float(rate), now)
    return float(rate)