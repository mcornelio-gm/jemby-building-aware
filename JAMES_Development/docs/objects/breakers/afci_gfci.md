# Object Specification: AFCI / GFCI Dual-Function Circuit Breaker

## 1. Overview
The **AFCI / GFCI Dual-Function Safety Circuit Breaker** (`AfciGfciBreakerObject`) combines thermal-magnetic overcurrent protection with advanced electronic microprocessors for Arc-Fault Circuit Interruption (AFCI per NEC 210.12) and Class A $5\text{mA}$ Ground-Fault Circuit Interruption (GFCI per NEC 210.8). It provides comprehensive fire and shock personnel protection for residential dwelling units and commercial wet/living areas.

* **Class**: `AfciGfciBreakerObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **AFCI Protection**: Detects dangerous parallel and series arcing signatures in damaged conductors or loose cords (NEC 210.12).
* **GFCI Protection**: Class A personnel protection tripping on $4\text{mA} - 6\text{mA}$ ground fault leakage within milliseconds (NEC 210.8).
* **Self-Test**: Continuous periodic automatic electronic diagnostic testing.
* **Available Poles**: 1-Pole ($120\text{V}$, 15A/20A) or 2-Pole ($120/240\text{V}$, 15A–50A for multi-wire branch circuits or heavy appliances).
* **Neutral Connection**: Plug-on Neutral (PoN) or coiled neutral pigtail wire.
* **Compatible Enclosures**: `ResidentialLoadcenterObject`, `LightingBranchPanelObject`.

---

## 3. Deterministic Rules & Validation
1. **Pole Restriction**: Validates that dual-function AFCI/GFCI breakers are only configured as 1-Pole ($120\text{V}$) or 2-Pole ($240\text{V}$). Flags an error if assigned 3 poles.
2. **Residential Room Code Compliance**: Recommends AFCI/GFCI protection for living rooms, dining rooms, kitchens, bedrooms, bathrooms, laundries, and garages.

---

## 4. Python Example
```python
from james_app.core.breakers import AfciGfciBreakerObject, BreakerStatus

afci_bkr = AfciGfciBreakerObject(
    id="bkr_res_1",
    tag="CB-1",
    name="Kitchen Countertop Small Appliance Circuit",
    slot_start=1,
    poles=1,
    occupied_slots=[1],
    amps=20,
    is_afci=True,
    is_gfci=True,
    self_test_enabled=True,
    status=BreakerStatus.ON,
    connected_phases=["A"]
)
```
