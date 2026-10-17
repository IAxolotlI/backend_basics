TEMP_COLD = 0.0
RATE_BIG = 100.0

def warm_clothes(temp_c):
    return temp_c < TEMP_COLD


def expensive(rate):
    return rate > RATE_BIG


def strip_description(description):
    if description and description.strip():
        return description.strip()
    return "unknown"