
import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars


def test_invalid_routes():
    with pytest.raises(ValueError):
        process_walking_routes("invalid", 5.0)


def test_negative_transport_fee():
    with pytest.raises(ValueError):
        process_walking_routes([], -1.0)


def test_unconfirmed_route():
    routes = [{"route_confirmed": False}]
    assert process_walking_routes(routes, 5.0)["status"] == "ZERO_EARNINGS"


def test_standard_60_weekend():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_60",
        "is_weekend": True,
        "walks": [{"num_pets": 2, "needs_meds": True}]
    }]
    result = process_walking_routes(routes, 5.0)
    assert result == {"total_revenue": 56.0, "status": "COMPLETED"}


def test_express_multiple_pets():
    routes = [{
        "route_confirmed": True,
        "session_type": "express_15",
        "walks": [{"num_pets": 4}]
    }]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 41.4


def test_unknown_session():
    routes = [{"route_confirmed": True, "session_type": "unknown"}]
    assert process_walking_routes(routes, 5.0)["status"] == "ZERO_EARNINGS"


def test_invalid_pet_count():
    routes = [{
        "route_confirmed": True,
        "walks": [{"num_pets": 0}]
    }]
    assert process_walking_routes(routes, 5.0)["status"] == "ZERO_EARNINGS"


def test_aggression_standard_60():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_60",
        "walks": [{"num_pets": 1, "aggression_alert": True}]
    }]
    assert process_walking_routes(routes, 5.0)["status"] == "ZERO_EARNINGS"


def test_aggression_standard_30():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "walks": [{"num_pets": 1, "aggression_alert": True}]
    }]
    assert process_walking_routes(routes, 5.0)["total_revenue"] == 0.0


def test_incident_audit():
    routes = [{
        "route_confirmed": True,
        "walks": [{"num_pets": 0} for _ in range(5)]
    }]
    assert process_walking_routes(routes, 5.0)["status"] == "INCIDENT_AUDIT"


def test_gps_no_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_online():
    assert inspect_gps_collars([[80, 60, 90]]) == "ONLINE"


def test_gps_lost_signal():
    assert inspect_gps_collars([[10, 15]]) == "LOST_SIGNAL_ALERT"


def test_gps_signal_recovery():
    assert inspect_gps_collars([[10, 80, 15]]) == "ONLINE"
