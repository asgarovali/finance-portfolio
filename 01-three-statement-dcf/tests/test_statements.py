import pandas as pd

from src.data import clean_statements as cs
from src.data.ixbrl import read_facts

IXBRL = """<html><body>
<ix:header><ix:resources>
<xbrli:context id="FY25"><xbrli:entity><xbrli:identifier>1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
<xbrli:context id="I25"><xbrli:entity><xbrli:identifier>1</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="FY25_seg"><xbrli:entity><xbrli:identifier>1</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="us-gaap:StatementBusinessSegmentsAxis">gva:MaterialsMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
</ix:resources></ix:header>
<table>
<tr><td>Revenue</td><td><ix:nonFraction name="us-gaap:Revenues" contextRef="FY25" unitRef="usd" scale="3">1,234</ix:nonFraction></td></tr>
<tr><td>Revenue again in a note</td><td><ix:nonFraction name="us-gaap:Revenues" contextRef="FY25" unitRef="usd" scale="3">1,234</ix:nonFraction></td></tr>
<tr><td>Other costs</td><td>(<ix:nonFraction name="us-gaap:OtherOperatingIncomeExpenseNet" contextRef="FY25" unitRef="usd" scale="3" sign="-">41</ix:nonFraction>)</td></tr>
<tr><td>Preferred</td><td><ix:nonFraction name="us-gaap:PreferredStockValue" contextRef="I25" unitRef="usd" format="ixt:fixed-zero">&#8212;</ix:nonFraction></td></tr>
<tr><td>Materials</td><td><ix:nonFraction name="us-gaap:Revenues" contextRef="FY25_seg" unitRef="usd" scale="6">0.5</ix:nonFraction></td></tr>
</table></body></html>"""


def test_read_facts(tmp_path):
    path = tmp_path / "f.htm"
    path.write_text(IXBRL, encoding="utf-8")
    f = read_facts(path).set_index(["tag", "dims"])

    assert len(f) == 4  # duplicate revenue tag dropped
    assert f.loc[("us-gaap:Revenues", ""), "value"] == 1_234_000
    assert f.loc[("us-gaap:OtherOperatingIncomeExpenseNet", ""), "value"] == -41_000
    assert f.loc[("us-gaap:PreferredStockValue", ""), "value"] == 0
    assert pd.isna(f.loc[("us-gaap:PreferredStockValue", ""), "start"])
    seg = "us-gaap:StatementBusinessSegmentsAxis=gva:MaterialsMember"
    assert f.loc[("us-gaap:Revenues", seg), "value"] == 500_000


def _fact(tag, value, accession, filed, start="2025-01-01"):
    return dict(tag=tag, start=start, end="2025-12-31", dims="", unit="usd",
                value=value, accession=accession, form="10-K", filed=filed)


def test_build_uses_latest_filing_and_signs(monkeypatch):
    monkeypatch.setattr(cs, "STATEMENTS", {"IS": [
        cs.item("Revenue", "us-gaap:Revenues"),
        cs.item("Cost of revenue", "us-gaap:CostOfGoodsAndServicesSold", -1),
        cs.total("Gross profit", ["Revenue", "Cost of revenue"], "us-gaap:GrossProfit"),
    ]})
    monkeypatch.setattr(cs, "ANCHOR", {"IS": "us-gaap:Revenues"})
    monkeypatch.setattr(cs, "periods", lambda: {"FY2025": ("2025-01-01", "2025-12-31")})
    facts = pd.DataFrame([
        # original filing
        _fact("us-gaap:Revenues", 90e6, "old", "2026-02-01"),
        _fact("us-gaap:CostOfGoodsAndServicesSold", 60e6, "old", "2026-02-01"),
        _fact("us-gaap:GrossProfit", 30e6, "old", "2026-02-01"),
        # later filing with recast figures
        _fact("us-gaap:Revenues", 100e6, "new", "2027-02-01"),
        _fact("us-gaap:CostOfGoodsAndServicesSold", 70e6, "new", "2027-02-01"),
        _fact("us-gaap:GrossProfit", 30e6, "new", "2027-02-01"),
    ])
    out = cs.build(facts).set_index("line")

    assert set(out["accession"]) == {"new"}
    assert out.loc["Cost of revenue", "value"] == -70
    assert out.loc["Gross profit", "value"] == out.loc["Gross profit", "filed_total"] == 30
