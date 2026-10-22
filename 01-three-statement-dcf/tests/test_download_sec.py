import json

import pytest

from src.data.download_sec import filings_index


def _submissions(tmp_path, rows):
    keys = ["form", "filingDate", "reportDate", "accessionNumber", "primaryDocument"]
    recent = {k: [r[i] for r in rows] for i, k in enumerate(keys)}
    path = tmp_path / "subs.json"
    path.write_text(json.dumps({"filings": {"recent": recent}}))
    return path


def test_keeps_periodic_reports_in_date_order(tmp_path):
    path = _submissions(tmp_path, [
        ("10-Q", "2021-05-07", "2021-03-31", "a2", "q.htm"),
        ("8-K", "2021-04-01", "", "a3", "8k.htm"),
        ("10-K", "2021-02-22", "2019-12-31", "a1", "k.htm"),
        ("10-K", "2017-02-20", "2016-12-31", "a0", "old.htm"),
    ])
    df = filings_index(path)
    assert list(df["accessionNumber"]) == ["a1", "a2"]


def test_raises_if_history_too_short(tmp_path):
    path = _submissions(tmp_path, [("10-K", "2022-02-28", "2021-12-31", "a1", "k.htm")])
    with pytest.raises(RuntimeError):
        filings_index(path)
