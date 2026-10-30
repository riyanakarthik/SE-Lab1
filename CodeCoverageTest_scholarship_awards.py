"""Tests aimed at LINE (code) coverage of scholarship_awards.py."""

import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# ---------- award_amount ----------
def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_negative_marks_raises():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_renewal_low_income_big_margin():
    # cutoff 75 - 5 = 70, above = 25 (> 15), rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 95, "low", True) == 4000


def test_non_low_income_small_margin():
    # cutoff 75, above = 5, rate = 60
    assert award_amount("merit", 80, "high", False) == 300


# ---------- is_eligible ----------
def test_is_eligible():
    assert is_eligible(90, 0, False) is True


def test_special_quota_too_many_backlogs():
    assert is_eligible(50, 3, True) is False


def test_low_attendance_not_eligible():
    assert is_eligible(60, 0, False) is False


# ---------- application_status ----------
def test_status_open_renewal_paper():
    # cutoff = 30 + 10 = 40, days_left 45 >= 40
    assert application_status(45, True, True) == "open"


def test_status_closing():
    # cutoff = 20, 10 >= 20 - 15
    assert application_status(10, False, False) == "closing"


def test_status_closed():
    assert application_status(2, False, False) == "closed"
