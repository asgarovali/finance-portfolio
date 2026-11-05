# Setup

Python 3.11 or newer.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Copy `.env.example` to `.env` and fill in a free FRED API key and a contact email for the SEC User-Agent. Each project then runs with `python -m src.run` from its own folder.

## Project layout

Each project is a separate folder with its own README, data sources (`data/SOURCES.md`), code and outputs. Code is MIT-licensed (see `LICENSE`).
