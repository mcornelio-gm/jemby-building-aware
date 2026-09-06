# Object Specification: Solar Photovoltaic (PV) System

## 1. Overview
The **Solar PV System Object** (`SolarPvSystemObject`) represents commercial and industrial grid-interactive solar photovoltaic arrays and inverters conforming to **NEC 690** and **NEC 705**. It defines total DC array capacity ($\text{kW-DC}$), AC continuous inverter capacity ($\text{kW-AC}$), MPPT operating windows, rapid shutdown compliance (NEC 690.12), and anti-islanding protection (IEEE 1547).

* **Class**: `SolarPvSystemObject`
* **Parent**: `PowerSourceObject`
* **Category**: `Renewable Generation`

---

## 2. Technical Specifications
* **DC System Capacity**: Nameplate solar string wattage in $\text{kW-DC}$.
* **Inverter AC Capacity**: Continuous grid-export capacity in $\text{kW-AC}$.
* **Inverter Efficiency**: CEC weighted efficiency ($\ge 98.0\%$).
* **Rapid Shutdown**: Module-level rapid shutdown initiator (NEC 690.12).
* **Anti-Islanding**: UL 1741 / IEEE 1547 utility loss trip.

---

## 3. Python Example
```python
from james_app.core.sources import SolarPvSystemObject

solar = SolarPvSystemObject(
    id="src_pv_1",
    tag="PV-1",
    name="Rooftop Solar Array",
    voltage=480.0,
    phases=3,
    capacity_kw=250.0,
    capacity_kva=250.0,
    dc_system_capacity_kw=300.0,
    inverter_ac_capacity_kw=250.0,
    has_rapid_shutdown=True
)
```
