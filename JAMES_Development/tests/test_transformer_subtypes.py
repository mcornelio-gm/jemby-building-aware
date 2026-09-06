"""Unit tests for Transformer Object Hierarchy and Sizing Calculations."""

import pytest
from james_app.core.transformers import (
    TransformerObject,
    DryTypeStepDownTransformerObject,
    LiquidFilledPadmountTransformerObject,
    IsolationTransformerObject,
    BuckBoostTransformerObject,
    WindingConfiguration,
    CoolingType,
)


def test_base_transformer_physics_and_rules():
    """Test 3-phase FLA, secondary short-circuit current, and NEC 450 protection sizing."""
    xfmr = TransformerObject(
        id="xfmr_t1",
        tag="T-1",
        name="Main Step-Down Transformer",
        kva_rating=75.0,
        primary_voltage=480.0,
        secondary_voltage=208.0,
        secondary_neutral_voltage=120.0,
        primary_phases=3,
        secondary_phases=3,
        winding_config=WindingConfiguration.DELTA_WYE,
        impedance_pct_z=5.0
    )

    # I_pri_fla = 75 * 1000 / (sqrt(3) * 480) = 90.21 A
    assert abs(xfmr.primary_full_load_amps - 90.21) < 0.1
    # I_sec_fla = 75 * 1000 / (sqrt(3) * 208) = 208.18 A
    assert abs(xfmr.secondary_full_load_amps - 208.18) < 0.1
    # I_sc = 208.18 / 0.05 = 4163.6 A
    assert abs(xfmr.max_secondary_short_circuit_amps - 4163.6) < 1.0

    # NEC 450 sizing calculations
    prot = xfmr.calculate_nec_450_max_primary_protection(has_secondary_protection=True)
    assert prot["multiplier"] == 2.50
    assert abs(prot["max_primary_ocpd_amps"] - (90.21 * 2.5)) < 1.0

    # Terminals
    assert "H1" in xfmr.get_input_ports()
    assert "X0" in xfmr.get_output_ports()
    assert "X1" in xfmr.get_output_ports()

    # Projections
    dot = xfmr.compile_focused_dot()
    assert "Transformer_xfmr_t1" in dot
    assert "480V 3Ø" in dot

    html_card = xfmr.render_html_view()
    assert "75.0 kVA" in html_card

    puml = xfmr.compile_plantuml_sld()
    assert "75.0 kVA" in puml

    # Rules
    assert len(xfmr.validate_rules()) == 0


def test_dry_type_step_down_transformer():
    """Test commercial dry-type transformer subclass."""
    dry_xfmr = DryTypeStepDownTransformerObject(
        id="xfmr_dry_1",
        tag="T-LP1",
        name="Lighting Transformer",
        kva_rating=45.0,
        primary_voltage=480.0,
        secondary_voltage=208.0,
        temperature_rise_c=150,
        winding_material="Copper",
        has_electrostatic_shield=True
    )
    assert dry_xfmr.transformer_type_name == "Dry-Type Step-Down Transformer"
    assert dry_xfmr.cooling_type == CoolingType.ANN_AIR
    assert len(dry_xfmr.validate_rules()) == 0


def test_liquid_filled_padmount_transformer():
    """Test outdoor padmount medium-to-low voltage transformer."""
    padmount = LiquidFilledPadmountTransformerObject(
        id="xfmr_pad_1",
        tag="PMTR-1",
        name="Campus Main Padmount Substation",
        kva_rating=1500.0,
        primary_voltage=12470.0,
        secondary_voltage=480.0,
        secondary_neutral_voltage=277.0,
        dielectric_fluid="FR3 (Less-Flammable Seed Oil)",
        is_dead_front=True,
        has_bayonet_fusing=True
    )
    assert padmount.primary_voltage == 12470.0
    # I_pri_fla = 1500 * 1000 / (sqrt(3) * 12470) = 69.45 A
    assert abs(padmount.primary_full_load_amps - 69.45) < 0.1
    # I_sec_fla = 1500 * 1000 / (sqrt(3) * 480) = 1804.22 A
    assert abs(padmount.secondary_full_load_amps - 1804.22) < 0.5
    assert len(padmount.validate_rules()) == 0


def test_isolation_and_buck_boost_transformers():
    """Test clean power isolation and buck-boost transformers."""
    iso = IsolationTransformerObject(
        id="xfmr_iso_1",
        tag="ISO-1",
        name="Data Center Clean Power Isolation Transformer",
        kva_rating=50.0,
        primary_voltage=480.0,
        secondary_voltage=208.0,
        k_factor=13,
        common_mode_attenuation_db=120
    )
    assert iso.k_factor == 13
    assert len(iso.validate_rules()) == 0

    bb = BuckBoostTransformerObject(
        id="xfmr_bb_1",
        tag="BB-1",
        name="208V to 230V Equipment Booster",
        kva_rating=5.0,
        autotransformer_load_kva=45.0,
        primary_voltage=208.0,
        secondary_voltage=230.0,
        boost_buck_percentage=10.58
    )
    assert bb.secondary_voltage == 230.0
    assert len(bb.validate_rules()) == 0
