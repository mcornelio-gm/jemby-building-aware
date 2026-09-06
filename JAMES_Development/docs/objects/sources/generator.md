# Object Specification: Emergency / Standby Diesel Generator

## 1. Overview
The **Diesel Generator Object** (`DieselGeneratorObject`) models emergency and standby engine-generator sets providing backup power per **NEC 700 / 701** and **NFPA 110 Class 10**. It incorporates quick 10-second start response times, sub-base UL 142 fuel storage autonomy calculations, fuel burn rates (GPH), and acoustic sound attenuation enclosures.

* **Class**: `DieselGeneratorObject`
* **Parent**: `PowerSourceObject`
* **Category**: `Emergency Generation`

---

## 2. Technical Specifications
* **Fuel Types (`FuelType`)**: Diesel #2, Natural Gas, LP Propane, Dual Fuel.
* **Fuel Autonomy**:
  $$\text{Autonomy (Hours)} = \frac{\text{Fuel Tank Capacity (Gallons)}}{\text{Full Load Burn Rate (GPH)}}$$
* **Starting Time**: $\le 10.0\text{ seconds}$ for NFPA 110 Type 10 emergency life safety systems.
* **Capacities**: $100\text{ kW} - 3000\text{ kW}+$.

---

## 3. Python Example
```python
from james_app.core.sources import DieselGeneratorObject, FuelType

gen = DieselGeneratorObject(
    id="src_gen_1",
    tag="GEN-1",
    name="Emergency Standby Generator",
    voltage=480.0,
    phases=3,
    capacity_kw=1000.0,
    capacity_kva=1250.0,
    fuel_type=FuelType.DIESEL,
    fuel_tank_capacity_gallons=1000.0,
    fuel_burn_rate_gph=70.0,
    starting_time_seconds=9.0
)
```
