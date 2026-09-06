# Object Specification: Battery Energy Storage System (BESS)

## 1. Overview
The **Battery Energy Storage System (BESS)** (`BatteryEnergyStorageObject`) represents electrochemical energy storage installations (Lithium Iron Phosphate / LFP) coupled with 4-quadrant bidirectional inverters. It provides peak shaving, microgrid islanding, frequency regulation, and emergency ride-through buffering.

* **Class**: `BatteryEnergyStorageObject`
* **Parent**: `PowerSourceObject`
* **Category**: `Energy Storage`

---

## 2. Technical Specifications
* **Capacity**: Total energy storage in $\text{kWh}$ and continuous power in $\text{kW}$.
* **Discharge Duration**:
  $$\text{Duration (Hours)} = \frac{\text{Usable Capacity (kWh)}}{\text{Power Rating (kW)}}$$
* **C-Rate**: Charge/discharge rate (e.g. $0.5\text{C}$ for 2-hour duration).
* **State of Charge (SOC)**: Real-time battery charge percentage ($0\% - 100\%$).

---

## 3. Python Example
```python
from james_app.core.sources import BatteryEnergyStorageObject

bess = BatteryEnergyStorageObject(
    id="src_bess_1",
    tag="BESS-1",
    name="Facility Peak-Shaving Battery Storage",
    voltage=480.0,
    phases=3,
    capacity_kw=500.0,
    capacity_kva=500.0,
    energy_capacity_kwh=1000.0,
    usable_capacity_kwh=900.0,
    power_rating_kw=500.0,
    state_of_charge_pct=85.0
)
```
