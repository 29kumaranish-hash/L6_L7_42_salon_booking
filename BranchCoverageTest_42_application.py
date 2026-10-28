"""Tests targeting both outcomes of decision branches in salon_booking.py."""
import pytest

from salon_booking import extra_time_charge, can_book, arrival_status


# service validation: unknown and known service
@pytest.mark.parametrize("service", ["unknown", "haircut"])
def test_service_validation_branch(service):
    if service == "unknown":
        with pytest.raises(ValueError, match="unknown service"):
            extra_time_charge(service, 20, "junior", False)
    else:
        assert extra_time_charge(service, 20, "junior", False) == 0


# duration validation: negative and non-negative
@pytest.mark.parametrize("duration", [-1, 0])
def test_duration_validation_branch(duration):
    if duration < 0:
        with pytest.raises(ValueError, match="invalid duration"):
            extra_time_charge("haircut", duration, "junior", False)
    else:
        assert extra_time_charge("haircut", duration, "junior", False) == 0


# membership compound condition: non-member, member non-spa, member spa
@pytest.mark.parametrize(
    "service,member,duration,expected",
    [
        ("haircut", False, 40, 100),
        ("haircut", True, 40, 0),
        ("spa", True, 100, 100),
    ],
)
def test_membership_branches(service, member, duration, expected):
    assert extra_time_charge(service, duration, "junior", member) == expected


# extra <= 0 / > 0; junior / non-junior; extra > 60 / <= 60;
# senior / non-senior inside the >60 branch.
@pytest.mark.parametrize(
    "duration,level,expected",
    [
        (30, "junior", 0),
        (40, "junior", 100),
        (90, "junior", 600),
        (91, "regular", 1586),
        (91, "senior", 1830),
    ],
)
def test_charge_rate_and_threshold_branches(duration, level, expected):
    assert extra_time_charge("haircut", duration, level, False) == expected


# walk-in true/false, party size <=2, party size >4, services <=2
@pytest.mark.parametrize(
    "party_size,services,walk_in,expected",
    [
        (2, 1, True, True),
        (3, 1, True, False),
        (4, 2, False, True),
        (5, 1, False, False),
        (2, 3, False, False),
    ],
)
def test_booking_decision_branches(party_size, services, walk_in, expected):
    assert can_book(party_size, services, walk_in) is expected


# colour/non-colour, weekend/weekday, open/late/closed thresholds
@pytest.mark.parametrize(
    "minutes,is_colour,weekend,expected",
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
def test_arrival_status_decision_branches(minutes, is_colour, weekend, expected):
    assert arrival_status(minutes, is_colour, weekend) == expected
