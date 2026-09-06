# Object Specification: Busway Plug-In Tap-Off Unit (Bus Plug)

## 1. Overview
The **Busway Tap-Off Unit (Bus Plug)** (`BusTapOffUnitObject`) is a portable disconnect switch or molded case circuit breaker that mechanically stabs directly onto the energized copper/aluminum busbars of a host plug-in busway run. It provides localized branch overcurrent protection ($30\text{A} - 800\text{A}$) feeding downstream machine tools, subpanels, or crane rails.

* **Class**: `BusTapOffUnitObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Busway Tap-Off`

---

## 2. Technical Specifications
* **Overcurrent Protection**: Fusible knife switch or Molded Case Circuit Breaker (MCCB).
* **Trip Ratings**: $30\text{A}, 60\text{A}, 100\text{A}, 200\text{A}, 400\text{A}, 600\text{A}, 800\text{A}$.
* **Safety Interlock**: Mechanical door interlock preventing opening of the enclosure while the switch is in the ON position.

---

## 3. Python Example
```python
from james_app.core.distribution import BusTapOffUnitObject

bus_plug = BusTapOffUnitObject(
    id="tap_floor_3",
    tag="TAP-3F",
    name="3rd Floor Lighting Subpanel Bus Plug",
    breaker_or_switch_amps=225,
    poles=3,
    is_fusible=False,
    host_busway_id="busway_riser_1",
    tap_outlet_index=3
)
```
