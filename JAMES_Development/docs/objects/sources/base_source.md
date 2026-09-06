# Object Specification: Power Source (Base Generation Entity)

## 1. Overview
The **Power Source** base class (`PowerSourceObject`) represents energy generation and grid interconnections within the Digital Twin graph (utility services, backup diesel generators, solar PV systems, battery storage). It establishes system nominal voltage, operating frequency ($60\text{Hz}/50\text{Hz}$), apparent capacity ($\text{kVA}$), real power capacity ($\text{kW}$), continuous Full Load Amps ($\text{FLA}$), and available short-circuit fault current contribution ($I_{sc}$).

* **Class**: `PowerSourceObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Power Source`

---

## 2. Technical Specifications
* **Source Classifications (`SourceType`)**:
  * `UTILITY`: Electric Utility Grid Service Entrance
  * `GENERATOR`: Standby / Emergency Engine-Generator
  * `SOLAR_PV`: Solar Photovoltaic Array & Inverter
  * `BATTERY_BESS`: Battery Energy Storage System (BESS)
  * `WIND`: Wind Turbine Generator
  * `COGEN_CHP`: Combined Heat & Power (CHP) / Microturbine
* **Electrical Parameters**:
  * `voltage`: Nominal line-to-line output voltage (e.g. $480\text{V}, 208\text{V}, 120\text{V}, 12.47\text{kV}$)
  * `phases`: 3-Phase or 1-Phase
  * `capacity_kw` & `capacity_kva`: Active and apparent power output
  * `power_factor`: Operating power factor ($0.80 - 1.0$)
  * `available_fault_current_ka`: Available short-circuit contribution ($I_{sc}$)

---

## 3. Deterministic Physics & Formulas
$$\text{Full Load Amps (3Ø)} = \frac{\text{kVA} \times 1000}{\sqrt{3} \times V_{\text{line-to-line}}}$$

---

## 4. Python Example
```python
from james_app.core.sources import PowerSourceObject, SourceType

source = PowerSourceObject(
    id="src_main",
    tag="UTIL-1",
    name="Utility Grid Service Entrance",
    source_type=SourceType.UTILITY,
    voltage=480.0,
    phases=3,
    capacity_kw=2000.0,
    capacity_kva=2500.0,
    available_fault_current_ka=45.0
)
```
