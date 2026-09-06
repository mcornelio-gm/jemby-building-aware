# Object Specification: Lighting & Appliance Branch Panel (LP / RP)

## 1. Overview
The **Branch Lighting & Appliance Panelboard** distributes power to localized branch circuits, lighting controls, general wall receptacles, and small single-phase loads in commercial, institutional, and industrial facilities.

* **Class**: `LightingBranchPanelObject`
* **Parent**: `PanelboardObject`
* **Category**: `Branch Lighting & Receptacle Panel`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `120/208V 3Ø 4W` (Lighting & Receptacles) or `277/480V 3Ø 4W` (Commercial Fluorescent/LED & High-Bay Lighting)
* **Bus Continuous Ampacity**: `100A`, `125A`, `225A`, `400A`
* **Short-Circuit Rating (SCCR)**: `10kA`, `14kA`, `22kA`, `65kA`
* **Standard Space Counts**: `18`, `30`, `42`, `54`, `84` spaces

---

## 3. Physical Layout & Breaker Matching
* **Matched Breaker Type**: `MiniatureBreakerObject` (MCB) bolt-on (QOB/BQ) or plug-on (QO/Q).
* **Circuit Composition**: Dense array of **1-Pole (15A, 20A)** and **2-Pole (30A, 50A)** branch units.
* **Phase Bus Alternation**: Alternates rows $(A,A) \to (B,B) \to (C,C)$ across Left (Odd) and Right (Even) columns.

---

## 4. Deterministic Rules & Validation
1. **Branch Circuit Sizing**: Warns if individual branch breakers exceed $100\text{A}$ (which should be fed from an MDP).
2. **Continuous Load Limit (NEC 210.20)**: Receptacle and lighting continuous loads sized at $125\%$.
3. **Phase Load Balancing**: Automatically calculates per-phase amp totals to prevent neutral overload.

---

## 5. Python Example
```python
from james_app.core.panels import LightingBranchPanelObject, SystemType

lp = LightingBranchPanelObject.create_empty(
    panel_id="LP_1",
    tag="LP-1",
    name="1st Floor Lighting Panel",
    total_spaces=42,
    mains_rating_amps=225,
    system_type=SystemType.THREE_PHASE_208Y_120V
)

# Add 1-pole lighting circuit on slot 1
lp.add_branch_circuit(slot_start=1, description="Corridor LED Lighting", amps=20, poles=1)
```
