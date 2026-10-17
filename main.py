import argparse
import json
import sys
import uuid
import logging

from clients.http import ServiceError, NotFoundError, BadResponseError
from processing.service import build_city_summary

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True)
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s run_id={uuid.uuid4().hex[:8]} %(levelname)s %(message)s",
    )

    try:
        summary = build_city_summary(args.city, args.currency)
    except NotFoundError as e:
        print(f"Not found: {e}", file=sys.stderr)
        return 3
    except (ServiceError, BadResponseError) as e:
        print(f"Service unavailable: {e}", file=sys.stderr)
        return 4

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        w = summary["weather"]
        r = summary["rates"]
        print(f"City: {summary['city']}")
        print(f"Weather: {w['temp_c']:.1f}°C, {w['description']}")
        print(f"Warm clothes: {'Yes' if w['warm_clothes'] else 'No'}")
        print(f"{r['currency']} – RUB: {r['rate_to_rub']:.2f}")
        print(f"Expensive currency: {'Yes' if r['expensive'] else 'No'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())