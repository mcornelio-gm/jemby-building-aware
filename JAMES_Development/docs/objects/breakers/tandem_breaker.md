# Object Specification: Tandem / Twin Space-Saver Circuit Breaker

## 1. Overview
The **Tandem / Twin / Quad Space-Saver Circuit Breaker** (`TandemBreakerObject`) accommodates two independent single-pole branch circuits within a single 1-inch physical slot position on a panelboard bus stab (e.g. Circuit 1A and 1B sharing Slot 1). It is engineered for residential loadcenters and light commercial panels to expand circuit capacity without replacing the physical enclosure.

* **Class**: `TandemBreakerObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **Sub-Circuit Capacity**: 2 independent circuits (Twin) or 4 circuits (Quad / 2-Pole $240\text{V}$ across 2 slots).
* **Trip Ratings**: $15\text{A}/15\text{A}$, $15\text{A}/20\text{A}$, $20\text{A}/20\text{A}$, $30\text{A}/30\text{A}$.
* **Slot Consumption**: 1 physical 1-inch slot connecting to a single phase stab.
* **Compatible Enclosures**: `ResidentialLoadcenterObject` (Class CTL or non-CTL compliant slots).

---

## 3. Deterministic Rules & Validation
1. **Single Slot / Phase Sharing**: Validates `poles == 1` for twin breakers since both sub-circuits draw from the identical phase bus stab (e.g. Phase A).
2. **CTL Slot Rejection**: Validates that panelboard slot accepts tandem breakers without violating manufacturer bus stabs or NEC limits.

---

## 4. Python Example
```python
from james_app.core.breakers import TandemBreakerObject, BreakerStatus

twin_bkr = TandemBreakerObject(
    id="bkr_res_tandem_1",
    tag="CB-1A/1B",
    name="Guest Bedroom Lighting & Receptacles",
    slot_start=1,
    poles=1,
    occupied_slots=[1],
    amps=15,
    secondary_amps=20,
    secondary_name="Hallway & Foyer Lighting",
    sub_circuits_count=2,
    status=BreakerStatus.ON,
    connected_phases=["A"]
)
```
