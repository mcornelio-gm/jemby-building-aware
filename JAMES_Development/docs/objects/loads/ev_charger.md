# Object Specification: Electric Vehicle (EV) Charging Station (NEC 625)

## 1. Overview
The **EV Charging Station Object** (`EvChargingStationObject`) represents Electric Vehicle Supply Equipment (EVSE) installations including Level 2 AC commercial chargers ($208\text{V}/240\text{V}$, $32\text{A}-80\text{A}$) and Level 3 DC Fast Chargers ($480\text{V } 3\text{Ø}$, $50\text{kW}-350\text{kW}$) per **NEC Article 625**. EV charging is classified as a $100\%$ continuous load, requiring $125\%$ branch circuit and OCPD sizing per **NEC 625.41**.

* **Class**: `EvChargingStationObject`
* **Parent**: `LoadObject`
* **Category**: `EV Infrastructure`

---

## 2. Technical Specifications
* **Charger Levels (`EvChargerLevel`)**:
  * `LEVEL_2_AC`: Single-phase $208\text{V}/240\text{V}$ ($7.2\text{kW}-19.2\text{kW}$).
  * `DC_FAST_CHARGER`: 3-Phase $480\text{V}$ ($50\text{kW}-350\text{kW}$).
* **Continuous Duty Sizing (NEC 625.41)**:
  $$\text{Required Breaker Sizing} \ge 125\% \times \text{Continuous Rated Charging Current}$$
* **Smart Energy Management**: Automatic peak-demand shaving and dynamic power sharing across dual vehicle ports.

---

## 3. Python Example
```python
from james_app.core.loads import EvChargingStationObject, EvChargerLevel

ev_charger = EvChargingStationObject(
    id="evse_dual_1",
    tag="EVSE-1",
    name="Commercial Dual-Port Level 2 Charger",
    charger_level=EvChargerLevel.LEVEL_2_AC,
    voltage=208.0,
    phases=1,
    charging_ports_count=2,
    output_power_kw=19.2,
    rated_current_amps=40.0
)
# Required Breaker: 50A (40A * 1.25 = 50A)
```
