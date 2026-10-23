from src.data.extract_cap import parse_cap

# shapes of the two table layouts, cut down from the FY2025 10-K and the Q2 2026 10-Q
TENK = ("All CAP is in the Construction segment. December 31, 2025 2024 (dollars in thousands) "
        "Unearned revenue $ 4,123,113 59.2 % $ 3,584,378 67.7 % Other awards 2,846,259 40.8 1,711,689 32.3 "
        "Total $ 6,969,372 100.0 % $ 5,296,067 100.0 % December 31, 2025")
TENQ = ("All CAP is in the Construction segment. (dollars in thousands) June 30, 2026 March 31, 2026 "
        "December 31, 2025 Unearned revenue $ 5,056,462 68.2 % $ 4,930,788 68.8 % $ 4,123,113 59.2 % "
        "Other awards 2,362,368 31.8 2,238,394 31.2 2,846,259 40.8 "
        "Total $ 7,418,830 100.0 % $ 7,169,182 100.0 % $ 6,969,372 100.0 % (dollars in thousands)")


def test_parse_cap_10k():
    t = parse_cap(TENK).set_index("date")
    assert list(t.index.strftime("%Y-%m-%d")) == ["2025-12-31", "2024-12-31"]
    assert t.loc["2025-12-31", "cap"] == 6969.372
    assert t.loc["2024-12-31", "other_awards"] == 1711.689


def test_parse_cap_10q():
    t = parse_cap(TENQ).set_index("date")
    assert list(t.index.strftime("%Y-%m-%d")) == ["2026-06-30", "2026-03-31", "2025-12-31"]
    assert (abs(t["unearned_revenue"] + t["other_awards"] - t["cap"]) < 1e-6).all()
