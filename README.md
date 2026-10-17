# city_summary

CLI-tool: weather in city and current currency.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py --city Moscow
python main.py --city Moscow --currency EUR
python main.py --city Moscow --json
```

## Tests

```bash
python -m unittest discover -s tests
```