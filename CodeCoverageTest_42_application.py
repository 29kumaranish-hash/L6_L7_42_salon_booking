"""Tests intended to cover executable lines in salon_booking.py."""
import pytest

from salon_booking import extra_time_charge, can_book, arrival_status


@pytest.mark.parametrize(
    "service,duration,level,member,expected",
    [
        ("haircut", 20, "junior", False, 0),          # within included time
        ("haircut", 30, "junior", False, 0),          # exactly included time
        ("haircut", 50, "junior", False, 200),        # junior rate, <= 60 extra
        ("colour", 80, "senior", True, 90),           # member gets 15 extra included minutes
        ("spa", 100, "junior", True, 100),            # membership does not change spa
        ("colour", 130, "regular", False, 1820),      # non-junior rate, > 60 extra
        ("colour", 130, "senior", False, 2100),       # senior surcharge when > 60 extra
    ],
)
def test_extra_time_charge_valid_cases(service, duration, level, member, expected):
    assert extra_time_charge(service, duration, level, member) == expected


def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 20, "junior", False)


def test_extra_time_charge_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


@pytest.mark.parametrize(
    "party_size,services,walk_in,expected",
    [
        (1, 1, True, True),
        (2, 3, True, True),
        (3, 1, True, False),
        (4, 2, False, True),
        (5, 1, False, False),
        (2, 3, False, False),
    ],
)
def test_can_book_cases(party_size, services, walk_in, expected):
    assert can_book(party_size, services, walk_in) is expected


@pytest.mark.parametrize(
    "minutes_early,is_colour,is_weekend,expected",
    [
        (10, True, False, "open"),
        (9, True, False, "late"),
        (-6, True, False, "closed"),
        (5, False, False, "open"),
        (4, False, False, "late"),
        (-11, False, False, "closed"),
        (20, True, True, "open"),
        (19, True, True, "late"),
        (-1, False, True, "closed"),
    ],
)
def test_arrival_status_cases(minutes_early, is_colour, is_weekend, expected):
    assert arrival_status(minutes_early, is_colour, is_weekend) == expected
