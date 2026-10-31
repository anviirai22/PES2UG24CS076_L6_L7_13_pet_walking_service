
import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_walking_routes(None, 5)
    with pytest.raises(ValueError):
        process_walking_routes([], -1)


def test_empty_and_unconfirmed_routes():
    assert process_walking_routes([], 5)["status"] == "ZERO_EARNINGS"
    assert process_walking_routes(
        [{"route_confirmed": False}], 5
    )["status"] == "ZERO_EARNINGS"


@pytest.mark.parametrize("session,expected", [
    ("standard_60", 40.0),
    ("standard_30", 27.0),
    ("express_15", 19.0),
])
def test_session_types(session, expected):
    routes = [{
        "route_confirmed": True,
        "session_type": session,
        "walks": [{"num_pets": 1}]
    }]
    assert process_walking_routes(routes, 5)["total_revenue"] == expected


def test_unknown_session():
    routes = [{"route_confirmed": True, "session_type": "unknown"}]
    assert process_walking_routes(routes, 5)["status"] == "ZERO_EARNINGS"


def test_invalid_pets_and_incident_audit():
    routes = [{
        "route_confirmed": True,
        "walks": [{"num_pets": 0} for _ in range(5)]
    }]
    assert process_walking_routes(routes, 5)["status"] == "INCIDENT_AUDIT"


def test_aggression_standard_60_break():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_60",
        "walks": [
            {"num_pets": 1},
            {"num_pets": 1, "aggression_alert": True},
            {"num_pets": 2}
        ]
    }]
    assert process_walking_routes(routes, 5)["status"] == "ZERO_EARNINGS"


def test_aggression_other_session():
    routes = [{
        "route_confirmed": True,
        "session_type": "express_15",
        "walks": [{"num_pets": 1, "aggression_alert": True}]
    }]
    assert process_walking_routes(routes, 5)["total_revenue"] == 0.0


def test_multiple_pets_discount():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "walks": [{"num_pets": 4}]
    }]
    assert process_walking_routes(routes, 5)["total_revenue"] == 48.6


def test_medication_and_weekend():
    routes = [{
        "route_confirmed": True,
        "is_weekend": True,
        "walks": [{"num_pets": 2, "needs_meds": True}]
    }]
    assert process_walking_routes(routes, 5)["total_revenue"] == 43.0


def test_gps_no_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_online_and_recovery():
    assert inspect_gps_collars([[80, 70]]) == "ONLINE"
    assert inspect_gps_collars([[10, 80, 15]]) == "ONLINE"


def test_gps_lost_signal():
    assert inspect_gps_collars([[10, 15]]) == "LOST_SIGNAL_ALERT"
