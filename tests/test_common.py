import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook

from common import data, excel, style


class FakeResponse:
    content = b'{"ok": 1}'

    def raise_for_status(self):
        pass


def test_download_writes_meta_and_uses_cache(tmp_path, monkeypatch):
    calls = []

    def fake_get(url, params=None, headers=None, timeout=None):
        calls.append(url)
        return FakeResponse()

    monkeypatch.setattr(data.requests, "get", fake_get)
    dest = tmp_path / "raw" / "x.json"

    data.download("https://example.com/x", dest, params={"series_id": "DGS10", "api_key": "secret"})
    data.download("https://example.com/x", dest)  # second call should hit the cache

    assert len(calls) == 1
    meta = json.loads((tmp_path / "raw" / "x.json.meta.json").read_text())
    assert "api_key" not in meta["params"]
    assert len(data.retrieval_date(dest)) == 10


def test_missing_env_var_raises(monkeypatch):
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    try:
        data._env("FRED_API_KEY")
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError")


def test_save_png(tmp_path):
    style.use_style()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    style.add_source(fig, "Source: test")
    path = style.save(fig, "test", tmp_path)
    assert path.exists()
    plt.close(fig)


def test_excel_input_is_blue_and_formula_black():
    wb = Workbook()
    ws = wb.active
    excel.setup_sheet(ws)
    excel.put_input(ws, "B3", 0.05, excel.FMT_PCT, note="Damodaran ERP")
    excel.put_formula(ws, "B4", "=B3*2", excel.FMT_PCT)
    assert ws["B3"].font.color.rgb.endswith("0000FF")
    assert ws["B4"].font.color is None or ws["B4"].font.color.rgb in (None, "FF000000")
    assert ws["C3"].value == "Damodaran ERP"
    assert ws.freeze_panes == "B2"
    assert ws.sheet_view.showGridLines is False
