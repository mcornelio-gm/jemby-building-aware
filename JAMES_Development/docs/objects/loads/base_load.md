# Object Specification: Electrical Load (Base Load Entity)

## 1. Overview
The **Electrical Load** base class (`LoadObject`) represents power-consuming apparatus connected to branch circuits or subpanel feeders. It defines nominal voltage, active power ($\text{kW}$), apparent power ($\text{kVA}$), operating power factor, Full Load Amps ($\text{FLA}$), continuous duty multiplier ($125\%$ per NEC 210.19), and upstream breaker connectivity.

* **Class**: `LoadObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Electrical Load`

---

## 2. Technical Specifications
* **Load Classifications (`LoadType`)**:
  * `MOTOR`: Electric Motor / Rotating Machinery
  * `VFD`: Variable Frequency Drive Inverter
  * `HVAC`: Packaged Chiller / Rooftop Unit
  * `EV_CHARGER`: Electric Vehicle Supply Equipment
  * `LIGHTING`: Lighting Branch Circuit / Zone
  * `RECEPTACLE`: General Convenience Outlets / Appliances
  * `IT_SERVER`: Data Center Server Rack
* **Minimum Circuit Ampacity (MCA)**:
  $$\text{MCA} = \text{FLA} \times (1.25 \text{ if Continuous else } 1.0)$$

---

## 3. Python Example
```python
from james_app.core.loads import LoadObject, LoadType

load = LoadObject(
    id="load_receptacle_1",
    tag="REC-1",
    name="Office Receptacle Group",
    load_type=LoadType.RECEPTACLE,
    voltage=120.0,
    phases=1,
    power_kw=1.8,
    power_kva=2.0
)
```
