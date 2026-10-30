"""Tests aimed at BRANCH coverage of scholarship_awards.py.

Every decision is driven both True and False, including boundary values.
"""

import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# ---------- award_amount: validation branches ----------
def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_negative_marks_raises():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_zero_marks_is_valid():
    # marks == 0 must NOT raise (boundary of marks < 0)
    assert award_amount("merit", 0, "low", False) == 0


# ---------- award_amount: renewal cutoff branch ----------
def test_renewal_non_sports_reduces_cutoff():
    # merit cutoff 75 - 5 = 70, above = 5, rate = 60
    assert award_amount("merit", 75, "high", True) == 300


def test_renewal_sports_keeps_cutoff():
    # sports cutoff stays 60 even on renewal, above = 10, rate = 100
    assert award_amount("sports", 70, "low", True) == 1000


def test_not_renewal_keeps_cutoff():
    # arts cutoff 65, above = 1, rate = 60
    assert award_amount("arts", 66, "high", False) == 60


# ---------- award_amount: above <= 0 branch ----------
def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_exactly_at_cutoff_gives_zero():
    assert award_amount("merit", 75, "low", False) == 0


def test_one_above_cutoff_pays():
    assert award_amount("merit", 76, "low", False) == 100


# ---------- award_amount: income and bonus branches ----------
def test_low_income_rate():
    assert award_amount("merit", 80, "low", False) == 500


def test_non_low_income_rate():
    assert award_amount("merit", 80, "high", False) == 300


def test_bonus_boundary_exactly_15_has_no_bonus():
    # above == 15 is NOT > 15
    assert award_amount("merit", 90, "low", False) == 1500


def test_bonus_low_income():
    # above = 16, rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 91, "low", False) == 2560


def test_bonus_non_low_income():
    # above = 16, rate = 60 + 40 = 100
    assert award_amount("merit", 91, "high", False) == 1600


def test_renewal_low_income_big_margin():
    assert award_amount("merit", 95, "low", True) == 4000


# ---------- is_eligible ----------
def test_is_eligible():
    assert is_eligible(90, 0, False) is True


def test_special_quota_within_backlog_limit():
    assert is_eligible(10, 2, True) is True


def test_special_quota_too_many_backlogs():
    assert is_eligible(50, 3, True) is False


def test_low_attendance_not_eligible():
    assert is_eligible(74, 0, False) is False


def test_attendance_boundary_with_one_backlog():
    assert is_eligible(75, 1, False) is True


def test_regular_quota_too_many_backlogs():
    assert is_eligible(75, 2, False) is False


# ---------- application_status ----------
@pytest.mark.parametrize(
    "days_left, is_renewal, is_paper, expected",
    [
        # new, no paper: cutoff 20
        (20, False, False, "open"),
        (19, False, False, "closing"),
        (5, False, False, "closing"),
        (4, False, False, "closed"),
        # renewal, no paper: cutoff 30
        (30, True, False, "open"),
        (29, True, False, "closing"),
        (15, True, False, "closing"),
        (14, True, False, "closed"),
        # new, paper: cutoff 30
        (30, False, True, "open"),
        (14, False, True, "closed"),
        # renewal, paper: cutoff 40
        (40, True, True, "open"),
        (39, True, True, "closing"),
        (25, True, True, "closing"),
        (24, True, True, "closed"),
    ],
)
def test_application_status(days_left, is_renewal, is_paper, expected):
    assert application_status(days_left, is_renewal, is_paper) == expected
