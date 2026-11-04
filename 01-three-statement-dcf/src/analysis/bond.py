"""Yield to maturity of a fixed-coupon bond with a first coupon period that
doesn't match the regular schedule (here: issued 2 Jun, first coupon 15 Dec).

Used to check the ODDFYIELD formula in the workbook, not to replace it.
"""
from __future__ import annotations

from datetime import date

from scipy.optimize import brentq


def days360(d1: date, d2: date) -> int:
    """30/360 (US) day count, enough for coupon dates that avoid month-ends in February."""
    day1 = min(d1.day, 30)
    day2 = 30 if d2.day == 31 and day1 == 30 else d2.day
    return (d2.year - d1.year) * 360 + (d2.month - d1.month) * 30 + (day2 - day1)


def _add_months(d: date, months: int) -> date:
    m = d.month - 1 + months
    return date(d.year + m // 12, m % 12 + 1, d.day)


def ytm(clean_price: float, settle: date, issue: date, first_coupon: date, maturity: date,
        coupon: float, freq: int = 2) -> float:
    """Annual yield (compounded freq times a year) for a price per 100 of principal.

    Settlement must fall before the first coupon. The first coupon is paid for the
    whole period from the issue date, so it's longer than a regular coupon."""
    assert issue < settle < first_coupon < maturity
    period = 360 // freq
    cpn = 100 * coupon / freq
    dates = [first_coupon]
    while dates[-1] < maturity:
        dates.append(_add_months(dates[-1], 12 // freq))
    assert dates[-1] == maturity, "maturity is not on the coupon schedule"

    flows = [cpn * days360(issue, first_coupon) / period] + [cpn] * (len(dates) - 1)
    flows[-1] += 100
    accrued = cpn * days360(issue, settle) / period
    w = days360(settle, first_coupon) / period  # fraction of a period to the first coupon

    def gap(y: float) -> float:
        dirty = sum(cf / (1 + y / freq) ** (w + k) for k, cf in enumerate(flows))
        return dirty - accrued - clean_price

    return brentq(gap, -0.5, 1.0)
