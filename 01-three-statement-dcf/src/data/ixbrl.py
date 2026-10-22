"""Read the numeric facts out of an inline XBRL (iXBRL) filing.

Since 2019 10-Ks and 10-Qs are filed as HTML with the XBRL tags embedded
(<ix:nonFraction>). Parsing those directly gives every tagged number on the
face statements, including the company's own custom tags (gva:...), which the
SEC companyfacts API leaves out.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

import pandas as pd


def _local(tag: str) -> str:
    return tag.split(":")[-1]


class _IXParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.contexts: dict[str, dict] = {}
        self.facts: list[dict] = []
        self._ctx: dict | None = None
        self._ctx_field: str | None = None
        self._dim: str | None = None
        self._open: list[dict] = []  # nonFraction elements can be nested

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        name = _local(tag)
        if name == "context":
            self._ctx = {"id": a["id"], "start": None, "end": None, "dims": []}
        elif self._ctx is not None and name in ("startdate", "enddate", "instant"):
            self._ctx_field = name
        elif self._ctx is not None and name == "explicitmember":
            self._dim = a.get("dimension")
        elif tag == "ix:nonfraction":
            self._open.append({**a, "text": ""})

    def handle_data(self, data):
        if self._ctx_field:
            value = data.strip()
            if self._ctx_field == "startdate":
                self._ctx["start"] = value
            else:  # enddate or instant
                self._ctx["end"] = value
        elif self._dim:
            self._ctx["dims"].append(f"{self._dim}={data.strip()}")
        for f in self._open:
            f["text"] += data

    def handle_endtag(self, tag):
        name = _local(tag)
        if name == "context" and self._ctx is not None:
            self.contexts[self._ctx["id"]] = self._ctx
            self._ctx = None
        elif name in ("startdate", "enddate", "instant"):
            self._ctx_field = None
        elif name == "explicitmember":
            self._dim = None
        elif tag == "ix:nonfraction" and self._open:
            self.facts.append(self._open.pop())


def _value(fact: dict) -> float:
    text = fact["text"].strip().replace(",", "")
    # zero is often shown as a dash, tagged with format ixt:fixed-zero / zerodash
    if text in ("", "-", "—", "–") or "zero" in fact.get("format", "") or "dash" in fact.get("format", ""):
        return 0.0
    if "numwords" in fact.get("format", ""):
        return float("nan")  # "six", "three" etc. in note text; not needed here
    value = float(text) * 10 ** int(fact.get("scale", 0) or 0)
    return -value if fact.get("sign") == "-" else value


def read_facts(path: str | Path) -> pd.DataFrame:
    """All numeric facts in one iXBRL document, one row per tag/period/dimension."""
    parser = _IXParser()
    parser.feed(Path(path).read_text(encoding="utf-8", errors="ignore"))

    rows = []
    for f in parser.facts:
        ctx = parser.contexts[f["contextref"]]
        rows.append({
            "tag": f["name"],
            "start": ctx["start"],
            "end": ctx["end"],
            "dims": ";".join(sorted(ctx["dims"])),
            "unit": f.get("unitref", ""),
            "value": _value(f),
        })
    # the same number is often tagged twice (statement and note); keep one
    return pd.DataFrame(rows).drop_duplicates(["tag", "start", "end", "dims", "unit"]).reset_index(drop=True)
