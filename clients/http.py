import time
import requests

TIMEOUT = 8
RETRIES = 2
RETRY_STATUSES = {500, 502, 503, 504}

class ServiceError(Exception):
    pass

class NotFoundError(Exception):
    pass

class BadResponseError(Exception):
    pass

def _etry_after(resp):
    try:
        return float(resp.headers.get("Retry-After"))
    except (TypeError, ValueError):
        return None


def get_json(url, params=None):
    for attempt in range(RETRIES + 1):
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < RETRIES:
                time.sleep(2 ** attempt)
                continue
            raise ServiceError(url)
        
        if resp.status_code in RETRY_STATUSES or resp.status_code == 429:
            if attempt < RETRIES:
                delay = retry_after(resp) if resp.status_code == 429 else 2 ** attempt
                time.sleep(delay if delay is not None else 2 ** attempt)
                continue
            raise ServiceError(url)

        if resp.status_code == 404:
            raise NotFoundError(url)

        if not resp.ok:
            raise ServiceError(url)

        try:
            return resp.json()
        except ValueError:
            raise BadResponseError(url)

    raise ServiceError(url)