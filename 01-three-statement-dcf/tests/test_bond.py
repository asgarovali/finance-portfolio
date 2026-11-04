from datetime import date

import pytest

from src.analysis.bond import days360, ytm


def test_days360():
    assert days360(date(2026, 6, 2), date(2026, 12, 15)) == 193
    assert days360(date(2026, 9, 30), date(2026, 12, 15)) == 75
    assert days360(date(2026, 1, 31), date(2026, 3, 31)) == 60


def test_regular_bond_at_par_yields_its_coupon():
    # issued on a coupon date, so the "odd" first period is a normal one. Between coupon
    # dates the street convention (compound discounting, linear accrued) is a hair off par.
    y = ytm(100, date(2026, 7, 1), date(2026, 6, 15), date(2026, 12, 15), date(2034, 6, 15), 0.06375)
    assert y == pytest.approx(0.06375, abs=2e-5)


def test_discount_price_yields_more_than_coupon():
    y = ytm(96.648, date(2026, 9, 30), date(2026, 6, 2), date(2026, 12, 15), date(2034, 6, 15), 0.06375)
    assert 0.06375 < y < 0.075
