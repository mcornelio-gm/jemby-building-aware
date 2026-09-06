# Object Specification: Residential Loadcenter Panel

## 1. Overview
The **Residential Loadcenter** represents a split-phase ($120/240\text{V } 1\text{Ø } 3\text{W}$) panelboard engineered specifically for single-family residences, townhomes, and multi-family dwelling units. It incorporates modern residential safety standards including Plug-on Neutral (PoN) bus architecture, whole-home surge protection (SPD), and specialized AFCI/GFCI protection.

* **Class**: `ResidentialLoadcenterObject`
* **Parent**: `PanelboardObject`
* **Category**: `Residential Loadcenter`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `120/240V 1Ø 3W` (Split-Phase)
* **Bus Continuous Ampacity**: `100A`, `125A`, `150A`, `200A`, `225A`
* **Short-Circuit Rating (SCCR)**: `10kA`, `22kA`
* **Mains Type**: `MCB` (Main Circuit Breaker, standard) or `MLO` (Main Lugs Only for downstream subpanels)
* **Standard Space Counts**: `24`, `30`, `40`, `42` spaces
* **Neutral Architecture**: Plug-on Neutral (PoN) for pigtail-free AFCI/GFCI installation

---

## 3. Physical Layout & Breaker Matching
* **Matched Breaker Types**:
  * `AfciGfciBreakerObject`: Dual-function arc-fault / ground-fault breakers for living spaces, bedrooms, kitchens, and bathrooms (NEC 210.12 / NEC 210.8).
  * `MiniatureBreakerObject`: Standard 1-Pole (120V) and 2-Pole (240V) thermal-magnetic breakers for baseboard heaters, dryers, ranges, EV chargers.
  * `TandemBreakerObject`: Twin / Quad space-saver breakers (2 circuits in 1 slot) for circuit expansion in non-CTL or tandem-rated slots.
* **Phase Stab Alternation**: Split-phase alternating rows (Row 1: Phase A, Row 2: Phase B, Row 3: Phase A, Row 4: Phase B).

---

## 4. Deterministic Rules & Validation
1. **System Voltage Rule**: Asserts `system_type == SystemType.SINGLE_PHASE_120_240V`. Flags a warning if configured with 3-phase systems.
2. **AFCI/GFCI Protection Check**: Validates that standard residential branch circuits (receptacles, lighting) are equipped with arc-fault and ground-fault protection.
3. **Mains Capacity Rule**: Validates that service breaker rating does not exceed rated busbar ampacity.

---

## 5. Python Example
```python
from james_app.core.panels import ResidentialLoadcenterObject, SystemType
from james_app.core.breakers import BreakerStatus

# Create 200A Residential Loadcenter
res_panel = ResidentialLoadcenterObject.create_empty(
    panel_id="RES_MAIN",
    tag="LP-MAIN",
    name="Residential Main Service Panel",
    total_spaces=40,
    mains_rating_amps=200,
    system_type=SystemType.SINGLE_PHASE_120_240V
)

# Add AFCI/GFCI Bedroom and Kitchen circuits
res_panel.add_residential_circuit(
    slot_start=1,
    description="Master Bedroom Receptacles",
    amps=15,
    poles=1,
    is_afci_gfci=True
)

# Add 2-Pole 240V EV Charger circuit (spans Slots 2 and 4 on Phase A and B)
res_panel.add_breaker(
    slot_start=2,
    poles=2,
    amps=50,
    description="Level 2 EV Charger"
)
```
