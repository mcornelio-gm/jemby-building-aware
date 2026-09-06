"""JEMBY Digital Twin - Panel Class, Breaker Object Model, and Domain Rules Engine."""

from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field


class SystemType(str, Enum):
    """Electrical distribution system phase & voltage configuration."""
    THREE_PHASE_208Y_120V = "120/208V 3Ø 4W"
    THREE_PHASE_480Y_277V = "277/480V 3Ø 4W"
    SINGLE_PHASE_120_240V = "120/240V 1Ø 3W"


class MainsType(str, Enum):
    """Main overcurrent protection or lug configuration."""
    MCB = "MAIN BREAKER"
    MLO = "MAIN LUGS ONLY"


class BreakerStatus(str, Enum):
    """Operational status of a circuit position."""
    ON = "ON"
    OFF = "OFF"
    TRIPPED = "TRIPPED"
    SPARE = "SPARE"
    SPACE = "SPACE"


class BreakerObject(BaseModel):
    """Embedded circuit breaker object representing a branch protection unit."""
    breaker_id: str = Field(..., description="Unique identifier for the breaker unit")
    slot_start: int = Field(..., description="Starting (primary) slot number")
    poles: int = Field(default=1, ge=1, le=3, description="Number of poles (1, 2, or 3)")
    occupied_slots: List[int] = Field(default_factory=list, description="All occupied slot IDs")
    amps: int = Field(default=20, ge=0, description="Trip rating in Amperes (0 for spare/space)")
    description: str = Field(default="Unused", description="Load or circuit name description")
    status: BreakerStatus = Field(default=BreakerStatus.ON, description="Breaker operational status")
    target_load_id: Optional[str] = Field(default=None, description="Connected downstream load or asset ID")
    connected_phases: List[str] = Field(default_factory=list, description="Computed phases: ['A'], ['A', 'B'], etc.")


class DownstreamLoad(BaseModel):
    """Downstream connected endpoint load/asset representation."""
    load_id: str
    name: str
    rating_label: str
    kva: float = 0.0


class UpstreamFeed(BaseModel):
    """Upstream service or feeder power source."""
    source_id: str
    name: str
    voltage_label: str


class PanelTwin(BaseModel):
    """Electrical Panelboard Digital Twin Representation Model."""
    panel_id: str = Field(..., description="Unique Panel Identifier (e.g., 'MDP-1')")
    name: str = Field(default="DISTRIBUTION PANEL", description="Panel display title")
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_type: MainsType = Field(default=MainsType.MCB)
    mains_rating_amps: int = Field(default=400, description="Main breaker or lug rating in Amps")
    bus_amps: int = Field(default=400, description="Main busbar continuous rating in Amps")
    total_spaces: int = Field(default=42, description="Total physical slots (e.g. 18, 30, 42, 54, 72, 84)")
    breakers: Dict[int, BreakerObject] = Field(default_factory=dict, description="Map of slot_start -> BreakerObject")
    upstream_feed: Optional[UpstreamFeed] = Field(default=None)
    downstream_loads: Dict[str, DownstreamLoad] = Field(default_factory=dict)


# --- Deterministic Domain Rules Engine ---

STANDARD_SPACE_COUNTS = [18, 30, 42, 54, 72, 84]


def compute_slot_phase(slot: int, system_type: SystemType) -> str:
    """
    Compute the bus phase stab for a given slot number based on row-pair alternation.
    Row 1: Slots 1, 2 -> Phase A
    Row 2: Slots 3, 4 -> Phase B
    Row 3: Slots 5, 6 -> Phase C (for 3-phase) or Phase A (for 1-phase)
    """
    row = (slot - 1) // 2  # 0-indexed row number
    if system_type == SystemType.SINGLE_PHASE_120_240V:
        return "A" if (row % 2 == 0) else "B"
    else:
        phases = ["A", "B", "C"]
        return phases[row % 3]


def auto_size_panel(poles_used: int, buffer_pct: float = 0.20) -> int:
    """
    Auto-size commercial panel spaces given required poles, adding growth buffer.
    Snaps to the smallest standard space count in {18, 30, 42, 54, 72, 84}.
    """
    target = int(poles_used * (1.0 + buffer_pct))
    for count in STANDARD_SPACE_COUNTS:
        if count >= target and count >= poles_used:
            return count
    return STANDARD_SPACE_COUNTS[-1]


def get_occupied_slots(slot_start: int, poles: int) -> List[int]:
    """Return the list of vertically adjacent slot numbers on the same column."""
    # Left column is odd (+2 per step), Right column is even (+2 per step)
    return [slot_start + (i * 2) for i in range(poles)]


def create_empty_panel(
    panel_id: str,
    name: str = "DISTRIBUTION PANEL",
    total_spaces: int = 42,
    mains_rating_amps: int = 400,
    system_type: SystemType = SystemType.THREE_PHASE_208Y_120V,
    mains_type: MainsType = MainsType.MCB
) -> PanelTwin:
    """Create a new PanelTwin with all slots initialized to [SPARE]."""
    panel = PanelTwin(
        panel_id=panel_id,
        name=name,
        system_type=system_type,
        mains_type=mains_type,
        mains_rating_amps=mains_rating_amps,
        bus_amps=mains_rating_amps,
        total_spaces=total_spaces,
        breakers={}
    )

    # Initialize all slots as individual 1-pole SPARE positions
    for slot in range(1, total_spaces + 1):
        phase = compute_slot_phase(slot, system_type)
        panel.breakers[slot] = BreakerObject(
            breaker_id=f"bkr_{panel_id}_{slot}",
            slot_start=slot,
            poles=1,
            occupied_slots=[slot],
            amps=0,
            description=f"Unused :{slot}",
            status=BreakerStatus.SPARE,
            connected_phases=[phase]
        )

    return panel


def add_breaker_to_panel(
    panel: PanelTwin,
    slot_start: int,
    poles: int,
    amps: int,
    description: str,
    status: BreakerStatus = BreakerStatus.ON,
    target_load_id: Optional[str] = None
) -> PanelTwin:
    """
    Add or update a breaker in the panel, validating bounds, multi-pole alignment,
    and removing any replaced individual spare slots.
    """
    if slot_start < 1 or slot_start > panel.total_spaces:
        raise ValueError(f"Starting slot {slot_start} out of bounds (1..{panel.total_spaces})")

    occupied = get_occupied_slots(slot_start, poles)
    for s in occupied:
        if s > panel.total_spaces:
            raise ValueError(f"Breaker pole slot {s} exceeds panel capacity ({panel.total_spaces})")

    # Compute phases for all occupied poles
    phases = [compute_slot_phase(s, panel.system_type) for s in occupied]

    # Remove any existing breaker entries occupying these slots
    for existing_start in list(panel.breakers.keys()):
        bkr = panel.breakers[existing_start]
        if any(s in occupied for s in bkr.occupied_slots):
            del panel.breakers[existing_start]

    # Register the new breaker
    new_bkr = BreakerObject(
        breaker_id=f"bkr_{panel.panel_id}_{slot_start}",
        slot_start=slot_start,
        poles=poles,
        occupied_slots=occupied,
        amps=amps,
        description=description,
        status=status,
        target_load_id=target_load_id,
        connected_phases=phases
    )
    panel.breakers[slot_start] = new_bkr

    return panel
