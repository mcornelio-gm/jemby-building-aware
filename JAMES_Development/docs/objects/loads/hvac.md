# Object Specification: HVAC Packaged Equipment & Chillers (NEC 440)

## 1. Overview
The **HVAC Equipment Object** (`HvacEquipmentObject`) models packaged rooftop units (RTU), chillers, and split-system condensing units incorporating hermetic refrigerant motor-compressors per **NEC Article 440**. It utilizes manufacturer nameplate Minimum Circuit Ampacity (MCA) for feeder conductor sizing and Maximum Overcurrent Protection (MOCP) for breaker selection.

* **Class**: `HvacEquipmentObject`
* **Parent**: `LoadObject`
* **Category**: `Mechanical / HVAC`

---

## 2. Technical Specifications & Nameplate Ratings
* **Tonnage**: Cooling refrigeration capacity in Tons ($1\text{ Ton} = 12,000\text{ BTU/hr}$).
* **Minimum Circuit Ampacity (MCA)**:
  $$\text{MCA} = (1.25 \times \text{Compressor RLA}) + \sum \text{Other Fan FLA}$$
* **Maximum Overcurrent Protection (MOCP)**:
  $$\text{MOCP} \le (2.25 \times \text{Compressor RLA}) + \sum \text{Other Fan FLA}$$
* **Rated Load Amps (RLA)** & **Locked Rotor Amps (LRA)**.

---

## 3. Python Example
```python
from james_app.core.loads import HvacEquipmentObject

rtu = HvacEquipmentObject(
    id="load_rtu_1",
    tag="RTU-1",
    name="Rooftop Packaged HVAC Unit",
    tonnage=25.0,
    voltage=480.0,
    phases=3,
    mca_amps=48.5,
    mocp_amps=70,
    compressor_rla=34.0,
    fan_motor_fla=6.0
)
```
