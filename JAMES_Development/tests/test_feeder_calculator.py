"""
Unit tests for NEC Feeder Calculator & Voltage Drop Engine.
"""

import pytest
from james_app.core.feeder_calculator import (
    calculate_voltage_drop,
    suggest_feeder_conductors,
    get_egc_size,
    get_conduit_ac_impedance,
    NEC_310_16_AMPACITY
)


def test_nec_ampacity_lookups():
    assert NEC_310_16_AMPACITY["Cu"]["4/0 AWG"][75] == 230
    assert NEC_310_16_AMPACITY["Cu"]["500 kcmil"][75] == 380
    assert NEC_310_16_AMPACITY["Al"]["4/0 AWG"][75] == 180


def test_egc_lookups():
    assert get_egc_size(20, "Cu") == "#12 AWG Cu"
    assert get_egc_size(100, "Cu") == "#8 AWG Cu"
    assert get_egc_size(400, "Cu") == "#3 AWG Cu"
    assert get_egc_size(1200, "Cu") == "3/0 AWG Cu"


def test_ac_impedance():
    r_steel, x_steel = get_conduit_ac_impedance("500 kcmil", "Cu", "Steel")
    r_pvc, x_pvc = get_conduit_ac_impedance("500 kcmil", "Cu", "PVC")
    assert r_steel == 0.032
    assert r_pvc == 0.029
    assert x_steel == 0.039


def test_voltage_drop_3phase_compliant():
    # 480V 3-phase, 100A load, 100ft, 1/0 AWG Cu in EMT
    res = calculate_voltage_drop(
        voltage=480.0,
        current_amps=100.0,
        length_ft=100.0,
        conductor_size="1/0 AWG",
        material="Cu",
        sets=1,
        conduit_type="EMT",
        is_three_phase=True
    )
    assert res["status"] == "COMPLIANT"
    assert res["voltage_drop_pct"] < 3.0
    assert res["voltage_drop_volts"] > 0
    assert res["end_voltage"] < 480.0


def test_voltage_drop_excessive():
    # 208V 3-phase, 200A load, 800ft long run with undersized wire
    res = calculate_voltage_drop(
        voltage=208.0,
        current_amps=200.0,
        length_ft=800.0,
        conductor_size="3/0 AWG",
        material="Cu",
        sets=1,
        conduit_type="EMT",
        is_three_phase=True
    )
    assert res["status"] in ("ACCEPTABLE", "EXCESSIVE")
    assert res["voltage_drop_pct"] > 3.0


def test_suggest_feeder_conductors():
    # 400A at 480V, 150ft
    rec = suggest_feeder_conductors(
        amperage=400.0,
        voltage=480.0,
        length_ft=150.0,
        material="Cu",
        max_voltage_drop_pct=3.0
    )
    assert rec["sets"] >= 1
    assert "Cu" in rec["run_description"]
    assert rec["calculation"]["voltage_drop_pct"] <= 3.0
