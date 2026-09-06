"""Unit tests for Panel Digital Twin, Phase Rules, Sizing, and Focused DOT Compiler."""

import pytest
from james_app.panel_twin import (
    BreakerStatus,
    DownstreamLoad,
    MainsType,
    SystemType,
    UpstreamFeed,
    add_breaker_to_panel,
    auto_size_panel,
    compute_slot_phase,
    create_empty_panel,
)
from james_app.panel_compiler import compile_panel_to_dot


def test_compute_slot_phase_three_phase():
    """Test standard 3-phase bus stab alternation (Row 1: A, Row 2: B, Row 3: C, Row 4: A...)."""
    sys_type = SystemType.THREE_PHASE_208Y_120V
    assert compute_slot_phase(1, sys_type) == "A"
    assert compute_slot_phase(2, sys_type) == "A"
    assert compute_slot_phase(3, sys_type) == "B"
    assert compute_slot_phase(4, sys_type) == "B"
    assert compute_slot_phase(5, sys_type) == "C"
    assert compute_slot_phase(6, sys_type) == "C"
    assert compute_slot_phase(7, sys_type) == "A"
    assert compute_slot_phase(8, sys_type) == "A"


def test_compute_slot_phase_single_phase():
    """Test 1-phase / split-phase alternation (Row 1: A, Row 2: B, Row 3: A...)."""
    sys_type = SystemType.SINGLE_PHASE_120_240V
    assert compute_slot_phase(1, sys_type) == "A"
    assert compute_slot_phase(2, sys_type) == "A"
    assert compute_slot_phase(3, sys_type) == "B"
    assert compute_slot_phase(4, sys_type) == "B"
    assert compute_slot_phase(5, sys_type) == "A"
    assert compute_slot_phase(6, sys_type) == "A"


def test_auto_size_panel():
    """Test commercial panel space sizing with 20% growth buffer."""
    assert auto_size_panel(10) == 18  # 10 * 1.2 = 12 -> snaps to 18
    assert auto_size_panel(20) == 30  # 20 * 1.2 = 24 -> snaps to 30
    assert auto_size_panel(32) == 42  # 32 * 1.2 = 38.4 -> snaps to 42
    assert auto_size_panel(50) == 72  # 50 * 1.2 = 60 -> snaps to 72


def test_empty_panel_creation_and_dot():
    """Test that creating an empty 42-space panel initializes all slots to [SPARE] and compiles valid DOT."""
    panel = create_empty_panel(
        panel_id="MDP_42",
        name="Main Distribution Panel",
        total_spaces=42,
        mains_rating_amps=400,
        system_type=SystemType.THREE_PHASE_208Y_120V,
        mains_type=MainsType.MCB
    )

    assert len(panel.breakers) == 42
    assert panel.breakers[1].status == BreakerStatus.SPARE
    assert panel.breakers[42].status == BreakerStatus.SPARE

    dot = compile_panel_to_dot(panel)
    assert "MAIN DISTRIBUTION PANEL (42 SPACES)" in dot
    assert "[ 400A MAIN BREAKER - 120/208V 3Ø 4W ]" in dot
    assert '[SPARE] Unused :1' in dot
    assert '[SPARE] Unused :42' in dot
    assert 'BGCOLOR="#FEFCBF"' in dot


def test_populated_panel_multi_pole_rowspan():
    """Test multi-pole breaker placement and verify ROWSPAN attribute in generated DOT."""
    panel = create_empty_panel(
        panel_id="PANEL_B",
        name="Building 4 Panel",
        total_spaces=24,
        mains_rating_amps=200,
        system_type=SystemType.THREE_PHASE_208Y_120V
    )

    # Add 1P Breaker on Slot 1
    add_breaker_to_panel(panel, slot_start=1, poles=1, amps=20, description="Lighting Cir 1")
    
    # Add 3P Breaker on Slot 3 (occupies 3, 5, 7 on left column)
    add_breaker_to_panel(
        panel,
        slot_start=3,
        poles=3,
        amps=50,
        description="RTU-1 Heat Pump",
        target_load_id="rtu_1"
    )
    panel.downstream_loads["rtu_1"] = DownstreamLoad(
        load_id="rtu_1",
        name="RTU-1 Rooftop Unit",
        rating_label="50A 208V 3-Phase",
        kva=15.0
    )

    # Add 2P Breaker on Slot 18 (occupies 18, 20 on right column)
    add_breaker_to_panel(panel, slot_start=18, poles=2, amps=30, description="Water Heater")

    # Add Upstream Utility Feed
    panel.upstream_feed = UpstreamFeed(
        source_id="Utility_Grid",
        name="Utility Grid",
        voltage_label="120/208V Main"
    )

    dot = compile_panel_to_dot(panel)

    # Verify 3P breaker has ROWSPAN="3" and spanned slot label
    assert 'ROWSPAN="3"' in dot
    assert '3,5,7: RTU-1 Heat Pump (3P 50A)' in dot
    
    # Verify 2P breaker has ROWSPAN="2"
    assert 'ROWSPAN="2"' in dot
    assert 'Water Heater (2P 30A) :18,20' in dot

    # Verify edge connections
    assert "Utility_Grid -> Panel_PANEL_B:main" in dot
    assert "Panel_PANEL_B:ckt_3_5_7 -> Load_rtu_1" in dot
