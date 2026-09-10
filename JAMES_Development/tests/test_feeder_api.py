"""
Unit tests for Feeder API Endpoints and Database Persistence.
"""

import pytest
from fastapi.testclient import TestClient
from james_app.main import app
from james_app.feeders import get_facility_feeders, update_feeder_edge


@pytest.fixture
def client():
    return TestClient(app)


def test_api_get_feeders(client):
    res = client.get("/api/feeders")
    assert res.status_code == 200
    data = res.json()
    assert "feeders" in data
    assert isinstance(data["feeders"], list)
    if len(data["feeders"]) > 0:
        f0 = data["feeders"][0]
        assert "from_tag" in f0
        assert "to_tag" in f0
        assert "conductor_size" in f0
        assert "calculation" in f0
        assert "voltage_drop_pct" in f0["calculation"]


def test_api_calc_voltage_drop(client):
    payload = {
        "voltage": 480.0,
        "current_amps": 100.0,
        "length_ft": 100.0,
        "conductor_size": "1/0 AWG",
        "material": "Cu",
        "sets": 1,
        "conduit_type": "EMT",
        "is_three_phase": True
    }
    res = client.post("/api/feeders/calc-voltage-drop", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "voltage_drop_volts" in data
    assert "voltage_drop_pct" in data
    assert data["status"] == "COMPLIANT"


def test_api_feeder_standards(client):
    res = client.get("/api/feeders/standards")
    assert res.status_code == 200
    data = res.json()
    assert "gauges" in data
    assert "500 kcmil" in data["gauges"]
    assert "conduits" in data


def test_api_update_feeder(client):
    payload = {
        "from_tag": "MDP-1",
        "to_tag": "T-1",
        "cable_tag": "FDR-MDP1-T1-TEST",
        "conductor_size": "3/0 AWG",
        "material": "Cu",
        "sets": 1,
        "conduit_type": "EMT",
        "length_ft": 95.0,
        "notes": "Test field feeder run"
    }
    res = client.post("/api/feeders/update", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["feeder"]["cable_tag"] == "FDR-MDP1-T1-TEST"
    assert data["feeder"]["length_ft"] == 95.0
