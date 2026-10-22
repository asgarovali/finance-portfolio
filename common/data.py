"""Download helpers.

The downloaded file itself is the cache: if it already exists in data/raw/ we
don't fetch it again unless refresh=True. Next to every file I write a small
.meta.json with the URL and retrieval time, so SOURCES.md can quote the exact
retrieval date instead of me remembering it.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
SEC_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"


def _env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is empty. Put it in the .env file at the repo root.")
    return value


def download(url: str, dest: str | Path, params: dict | None = None,
             headers: dict | None = None, refresh: bool = False) -> Path:
    """Save the response body to dest untouched and return the path."""
    dest = Path(dest)
    if dest.exists() and not refresh:
        return dest

    resp = requests.get(url, params=params, headers=headers, timeout=60)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)

    # keep the API key out of the metadata file
    safe_params = {k: v for k, v in (params or {}).items() if k != "api_key"}
    meta = {
        "url": url,
        "params": safe_params,
        "retrieved_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }
    dest.with_name(dest.name + ".meta.json").write_text(json.dumps(meta, indent=2))
    return dest


def retrieval_date(path: str | Path) -> str:
    """Date (YYYY-MM-DD) a file was downloaded, read from its .meta.json."""
    path = Path(path)
    meta = json.loads(path.with_name(path.name + ".meta.json").read_text())
    return meta["retrieved_utc"][:10]


def fred_series(series_id: str, raw_dir: str | Path, refresh: bool = False) -> Path:
    """Download all observations of one FRED series as JSON."""
    params = {"series_id": series_id, "api_key": _env("FRED_API_KEY"), "file_type": "json"}
    return download(FRED_URL, Path(raw_dir) / f"fred_{series_id}.json", params=params, refresh=refresh)


def _sec_get(url: str, dest: Path, refresh: bool) -> Path:
    # SEC wants a User-Agent with a contact email and at most 10 requests/second
    headers = {"User-Agent": f"Ali Asgarov finance-portfolio {_env('SEC_EMAIL')}"}
    existed = dest.exists()
    path = download(url, dest, headers=headers, refresh=refresh)
    if refresh or not existed:
        time.sleep(0.2)
    return path


def sec_company_facts(cik: int, raw_dir: str | Path, refresh: bool = False) -> Path:
    """Download the XBRL companyfacts JSON for one company from SEC EDGAR."""
    dest = Path(raw_dir) / f"sec_companyfacts_{cik:010d}.json"
    return _sec_get(SEC_FACTS_URL.format(cik=cik), dest, refresh)


def sec_submissions(cik: int, raw_dir: str | Path, refresh: bool = False) -> Path:
    """Download the filing history (form types, dates, accession numbers)."""
    dest = Path(raw_dir) / f"sec_submissions_{cik:010d}.json"
    return _sec_get(SEC_SUBMISSIONS_URL.format(cik=cik), dest, refresh)


def sec_filing_doc(cik: int, accession: str, document: str, raw_dir: str | Path,
                   refresh: bool = False) -> Path:
    """Download one document of a filing from the EDGAR archive."""
    acc = accession.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{document}"
    return _sec_get(url, Path(raw_dir) / f"{accession}_{document}", refresh)
