"""Comprehensive test suite verifying all new Digital Twin object classes."""

import pytest
from james_app.core import (
    # Sources
    PowerSourceObject,
    SourceType,
    UtilityServiceSource,
    DieselGeneratorObject,
    SolarPvSystemObject,
    BatteryEnergyStorageObject,
    # Loads
    LoadObject,
    LoadType,
    ElectricMotorObject,
    VariableFrequencyDriveObject,
    HvacEquipmentObject,
    EvChargingStationObject,
    LumpedLoadObject,
    # Power Quality & UPS
    UpsObject,
    SurgeProtectiveDeviceObject,
    PowerDistributionUnitObject,
    PowerFactorCapacitorBankObject,
    # Distribution
    BuswayObject,
    BusTapOffUnitObject,
    CableTrayObject,
    # Protection
    ProtectiveRelayObject,
    CurrentTransformerObject,
    PotentialTransformerObject,
)


def test_power_sources():
    """Verify utility service, generator, solar PV, and BESS."""
    util = UtilityServiceSource(
        id="src_util_1",
        tag="UTIL-1",
        name="Utility Service Entrance",
        voltage=480.0,
        phases=3,
        capacity_kw=2000.0,
        capacity_kva=2500.0,
        available_fault_mva_sc=500.0,
        available_fault_current_ka=45.0
    )
    assert util.full_load_amps > 3000.0
    assert len(util.validate_rules()) == 0
    assert "Utility Grid Service" in util.compile_focused_dot()
    assert "UTIL-1" in util.render_html_view()

    gen = DieselGeneratorObject(
        id="src_gen_1",
        tag="GEN-1",
        name="Emergency Standby Generator",
        capacity_kw=1000.0,
        capacity_kva=1250.0,
        fuel_tank_capacity_gallons=1000.0,
        fuel_burn_rate_gph=70.0,
        starting_time_seconds=9.0
    )
    assert gen.fuel_autonomy_hours > 14.0
    assert len(gen.validate_rules()) == 0

    pv = SolarPvSystemObject(
        id="src_pv_1",
        tag="PV-1",
        name="Rooftop Solar Array",
        voltage=480.0,
        capacity_kw=250.0,
        capacity_kva=250.0,
        dc_system_capacity_kw=300.0,
        inverter_ac_capacity_kw=250.0,
        has_rapid_shutdown=True
    )
    assert len(pv.validate_rules()) == 0

    bess = BatteryEnergyStorageObject(
        id="src_bess_1",
        tag="BESS-1",
        name="Facility Battery Storage",
        capacity_kw=500.0,
        capacity_kva=500.0,
        energy_capacity_kwh=1000.0,
        usable_capacity_kwh=900.0,
        power_rating_kw=500.0
    )
    assert bess.duration_hours == 1.80
    assert len(bess.validate_rules()) == 0


def test_electrical_loads():
    """Verify motor, VFD, HVAC, EV charger, and lumped load."""
    motor = ElectricMotorObject(
        id="load_motor_1",
        tag="MTR-1",
        name="Chilled Water Pump Motor",
        horsepower_hp=50.0,
        voltage=480.0,
        phases=3
    )
    # 50HP at 460V is 65A per NEC Table 430.250
    assert motor.nec_table_fla == 65.0
    assert motor.branch_conductor_ampacity == 65.0 * 1.25
    assert motor.max_breaker_inverse_time_amps == 65.0 * 2.50
    assert len(motor.validate_rules()) == 0

    vfd = VariableFrequencyDriveObject(
        id="load_vfd_1",
        tag="VFD-1",
        name="Air Handler Supply Fan VFD",
        voltage=480.0,
        phases=3,
        motor_hp=30.0,
        rated_output_amps=40.0
    )
    assert len(vfd.validate_rules()) == 0

    hvac = HvacEquipmentObject(
        id="load_rtu_1",
        tag="RTU-1",
        name="Rooftop Packaged HVAC Unit",
        voltage=480.0,
        phases=3,
        tonnage=25.0,
        mca_amps=48.5,
        mocp_amps=70
    )
    assert len(hvac.validate_rules()) == 0

    ev = EvChargingStationObject(
        id="load_ev_1",
        tag="EVSE-1",
        name="Fleet Level 2 Dual EV Charger",
        voltage=208.0,
        phases=1,
        charging_ports_count=2,
        rated_current_amps=40.0
    )
    assert ev.required_breaker_amps == 50  # 40A * 1.25 = 50A
    assert len(ev.validate_rules()) == 0

    lumped = LumpedLoadObject(
        id="load_lighting_1",
        tag="LTG-ZONE-A",
        name="2nd Floor Office Lighting",
        voltage=277.0,
        phases=1,
        power_kw=12.0,
        power_kva=13.3,
        demand_factor_pct=100.0
    )
    assert lumped.diversified_power_kva == 13.3
    assert len(lumped.validate_rules()) == 0


def test_power_quality_and_ups():
    """Verify UPS, SPD, PDU, and capacitor bank."""
    ups = UpsObject(
        id="ups_dc_1",
        tag="UPS-1",
        name="Central Data Center UPS",
        capacity_kw=500.0,
        capacity_kva=500.0,
        input_voltage=480.0,
        output_voltage=480.0,
        battery_runtime_minutes_at_100pct=15.0
    )
    assert ups.output_full_load_amps > 600.0
    assert len(ups.validate_rules()) == 0

    spd = SurgeProtectiveDeviceObject(
        id="spd_main",
        tag="SPD-1",
        name="Main Service SPD",
        surge_capacity_ka_per_phase=200.0
    )
    assert len(spd.validate_rules()) == 0

    pdu = PowerDistributionUnitObject(
        id="pdu_pod_1",
        tag="PDU-1",
        name="Server Pod PDU",
        kva_rating=150.0,
        total_branch_poles=84
    )
    assert len(pdu.validate_rules()) == 0

    cap = PowerFactorCapacitorBankObject(
        id="pfc_main",
        tag="PFC-1",
        name="Main Bus Power Factor Capacitor Bank",
        rated_kvar=200.0,
        steps_count=8,
        has_detuning_reactors=True
    )
    assert len(cap.validate_rules()) == 0


def test_distribution_infrastructure_and_protection():
    """Verify busway, bus tap, cable tray, relay, CT, and PT."""
    busway = BuswayObject(
        id="busway_riser_1",
        tag="BUSWAY-1",
        name="East Wing Electrical Riser Busway",
        rated_amps=2000,
        voltage=480.0,
        length_ft=120.0
    )
    assert len(busway.validate_rules()) == 0

    tap = BusTapOffUnitObject(
        id="tap_floor_3",
        tag="TAP-3F",
        name="3rd Floor Bus Tap Disconnect",
        breaker_or_switch_amps=225,
        poles=3
    )
    assert len(tap.validate_rules()) == 0

    tray = CableTrayObject(
        id="tray_main_corr",
        tag="TRAY-1",
        name="Main Corridor Cable Tray",
        width_inches=24.0,
        depth_inches=6.0,
        current_fill_pct=42.0
    )
    assert len(tray.validate_rules()) == 0

    relay = ProtectiveRelayObject(
        id="relay_main_5051",
        tag="RELAY-52M",
        name="Main Breaker Feeder Protection Relay",
        relay_model="SEL-751",
        controls_breaker_id="CB-MAIN"
    )
    assert len(relay.validate_rules()) == 0

    ct = CurrentTransformerObject(
        id="ct_phase_a",
        tag="CT-A",
        name="Phase A Current Transformer",
        primary_ratio_amps=2000,
        secondary_ratio_amps=5
    )
    assert ct.ratio_str == "2000:5A"

    pt = PotentialTransformerObject(
        id="pt_bus",
        tag="PT-1",
        name="Bus Potential Transformer",
        primary_voltage=480.0,
        secondary_voltage=120.0
    )
    assert pt.ratio_str == "480V:120V"
