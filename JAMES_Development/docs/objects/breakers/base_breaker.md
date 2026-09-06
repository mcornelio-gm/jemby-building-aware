# Object Specification: Circuit Breaker (Base Protective Device)

## 1. Overview
The **Circuit Breaker** base class (`CircuitBreakerObject`) represents an overcurrent protective device (OCPD) installed within a panelboard or enclosure slot. It models physical slot attachments, pole counts ($1\text{P}, 2\text{P}, 3\text{P}$), continuous trip ratings ($15\text{A} - 6000\text{A}$), interrupting capacity ($\text{AIC}$ ratings), operational statuses, and phase stab connectivity.

* **Class**: `CircuitBreakerObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Protective Device`

---

## 2. Core Attributes
* **Operational Statuses (`BreakerStatus`)**:
  * `ON`: Normal closed operation carrying load current.
  * `OFF`: Manually opened / disconnected.
  * `TRIPPED`: Automatically opened due to overcurrent, short-circuit, or fault condition.
  * `SPARE`: Active physical breaker installed but unassigned to an active load.
  * `SPACE`: Empty physical chassis slot reserved for future breaker installation.
* **Continuous Trip Rating (`amps`)**: $15\text{A}, 20\text{A}, 30\text{A}, 50\text{A}, 100\text{A}, 225\text{A}, 400\text{A}, \dots$
* **Frame Rating (`frame_amps`)**: Physical chassis continuous rating (e.g. $100\text{A}, 250\text{A}, 800\text{A}$).
* **Interrupting Capacity (`aic_rating_ka`)**: Short-circuit rating in kiloamperes (e.g. $10\text{kA}, 22\text{kA}, 35\text{kA}, 65\text{kA}$).
* **Poles (`poles`)**: $1$, $2$, or $3$ poles.
* **Occupied Slots (`occupied_slots`)**: Array of integer slot IDs occupied on the panel chassis.
* **Connected Phases (`connected_phases`)**: List of phase legs energized by this breaker (e.g. `["A"]`, `["A", "B"]`, `["A", "B", "C"]`).

---

## 3. Terminal Connectivity & Ports
* **Input Ports**: `get_input_ports() -> List[str]` returns bus stab terminal identifiers `[f"bus_stab_{s}" for s in occupied_slots]`.
* **Output Ports**: `get_output_ports() -> List[str]` returns downstream circuit terminal `[f"ckt_{'_'.join(occupied_slots)}"]`.

---

## 4. Deterministic Rules & Validation
1. **Positive Trip Sizing**: Validates `amps >= 0`.
2. **Pole Range**: Validates `poles in [1, 2, 3]`.
3. **Slot Occupancy Match**: Asserts `len(occupied_slots) == poles`.
4. **Phase Distinctness**: Validates that multi-pole breakers connect across distinct phase stabs (e.g., $A-B$ or $A-B-C$, never $A-A$).

---

## 5. Visual Projections
* **Graphviz DOT**: Renders a compact record node with `<in> Line`, `<bkr> Name & Status`, and `<out> Load` ports.
* **Native HTML**: Color-coded interactive badge showing status pill (`[ON]`, `[OFF]`, `[SPARE]`), circuit slot tag, description, and trip rating.
* **PlantUML SLD**: Clean component box with schematic tag, amperage rating, and pole configuration.

---

## 6. Python Example
```python
from james_app.core.breakers import CircuitBreakerObject, BreakerStatus

bkr = CircuitBreakerObject(
    id="bkr_lp1_1",
    tag="CB-1",
    name="Office Lighting Branch",
    slot_start=1,
    poles=1,
    occupied_slots=[1],
    amps=20,
    status=BreakerStatus.ON,
    connected_phases=["A"]
)
```
