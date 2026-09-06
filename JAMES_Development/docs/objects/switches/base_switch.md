# Object Specification: Switch & Disconnect (Base Switching Apparatus)

## 1. Overview
The **Switch & Disconnect** base class (`SwitchObject`) models manual and automatic electrical contactors, safety disconnects, and transfer apparatus designed to establish, maintain, and interrupt power flow. It incorporates operational switch contact states (`CLOSED`, `OPEN`, `TRIPPED`), OSHA Lockout/Tagout (LOTO) safety attributes, NEMA environmental ratings, short-circuit withstand/interrupting ratings (SCCR), and line/load terminal connections.

* **Class**: `SwitchObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Switch & Disconnect`

---

## 2. Technical Specifications & Enclosures
* **Operating States (`SwitchState`)**:
  * `CLOSED`: Contacts mechanically engaged, conducting continuous current.
  * `OPEN`: Contacts isolated with visible air gap.
  * `TRIPPED`: Overcurrent or fault opening (on breaker/fused mechanisms).
* **NEMA Enclosure Ratings (`EnclosureNemaType`)**:
  * `NEMA 1`: General Indoor Commercial.
  * `NEMA 3R`: Outdoor Rainproof & Sleet Resistant.
  * `NEMA 4X`: Stainless Steel Watertight & Corrosion Resistant (Washdown/Food).
  * `NEMA 12`: Industrial Dust-Tight & Drip-Tight.
* **Continuous Ampacity**: $30\text{A}, 60\text{A}, 100\text{A}, 200\text{A}, 400\text{A}, 600\text{A}, 800\text{A}, 1200\text{A}$
* **Poles**: $1\text{P}, 2\text{P}, 3\text{P}, 4\text{P}$ (with switched or solid neutral).

---

## 3. Terminal Connectivity
* **Line-Side Inputs (`get_input_ports`)**: `["line_L1", "line_L2", "line_L3"]`
* **Load-Side Outputs (`get_output_ports`)**: `["load_T1", "load_T2", "load_T3"]`

---

## 4. Python Example
```python
from james_app.core.switches import SwitchObject, SwitchState, EnclosureNemaType

sw = SwitchObject(
    id="sw_main_disc",
    tag="SW-1",
    name="Main Service Disconnect",
    poles=3,
    rated_amps=200,
    voltage=480.0,
    state=SwitchState.CLOSED,
    enclosure_type=EnclosureNemaType.NEMA_3R
)
```
