# Object Specification: Miniature Circuit Breaker (MCB)

## 1. Overview
The **Miniature Circuit Breaker (MCB)** (`MiniatureBreakerObject`) represents standard 1-inch per pole branch circuit protective devices designed for lighting, receptacle, small motor, and appliance branch circuits ($15\text{A} - 60\text{A}$, up to $100\text{A}$). They are available in Bolt-On (QOB/BQ/BAB for commercial applications) and Plug-On (QO/Q/BR for residential/light commercial) mounting configurations.

* **Class**: `MiniatureBreakerObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **Nominal Amperage**: $15\text{A}, 20\text{A}, 30\text{A}, 40\text{A}, 50\text{A}, 60\text{A}, 70\text{A}, 100\text{A}$
* **Poles**: 1-Pole ($120\text{V}$ / $277\text{V}$), 2-Pole ($208\text{V}$ / $240\text{V}$ / $480\text{V}$), 3-Pole ($208\text{V}$ / $480\text{V}$)
* **Mounting Types**: `Bolt-On` (Commercial/Industrial NQ/NF) or `Plug-On`
* **Interrupting Capacity ($\text{AIC}$)**: $10\text{kA}$, $22\text{kA}$
* **Compatible Enclosures**: `LightingBranchPanelObject`, `SubpanelObject`, `EmergencyPanelObject`, `CriticalPowerPanelObject`, `ResidentialLoadcenterObject`.

---

## 3. Deterministic Rules & Validation
1. **Continuous Trip Limit**: Warns if trip rating exceeds $100\text{A}$, advising use of an industrial Molded Case Breaker (`MoldedCaseBreakerObject`).
2. **Mounting Integrity**: Verifies panel chassis mounting compatibility (e.g. Bolt-On required for critical commercial facilities).

---

## 4. Python Example
```python
from james_app.core.breakers import MiniatureBreakerObject, BreakerStatus

mcb = MiniatureBreakerObject(
    id="bkr_lp1_3",
    tag="CB-3",
    name="Corridor LED Lighting",
    slot_start=3,
    poles=1,
    occupied_slots=[3],
    amps=20,
    mounting_type="Bolt-On",
    aic_rating_ka=10.0,
    status=BreakerStatus.ON,
    connected_phases=["B"]
)
```
