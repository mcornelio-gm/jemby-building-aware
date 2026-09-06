# Object Specification: Uninterruptible Power Supply (UPS)

## 1. Overview
The **Uninterruptible Power Supply (UPS)** (`UpsObject`) represents online double-conversion, line-interactive, or rotary energy storage systems protecting mission-critical IT, data center, and healthcare facilities. It calculates rectifier input full-load current (including battery recharge allowance), inverter continuous output ampacity, battery autonomy runtime minutes at $100\%$ full load, and static/maintenance bypass routing.

* **Class**: `UpsObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Uninterruptible Power Supply`

---

## 2. Technical Specifications
* **Topologies (`UpsTopology`)**:
  * `DOUBLE_CONVERSION`: Online Double-Conversion (AC $\to$ DC $\to$ AC) with zero transfer time.
  * `LINE_INTERACTIVE`: Fast-switching voltage regulation UPS.
  * `ROTARY_FLYWHEEL`: Diesel/Flywheel dynamic kinetic energy ride-through.
* **Capacities**: $10\text{ kVA} - 2000\text{ kVA}+$.
* **Battery Autonomy**: Minutes of full-power runtime during grid outages ($5 - 60\text{ min}$).
* **Efficiency**: Online AC-to-AC efficiency ($95\% - 97\%$).

---

## 3. Python Example
```python
from james_app.core.power_quality import UpsObject, UpsTopology

ups = UpsObject(
    id="ups_datacenter_1",
    tag="UPS-1",
    name="Central Enterprise Data Center UPS",
    topology=UpsTopology.DOUBLE_CONVERSION,
    capacity_kw=500.0,
    capacity_kva=500.0,
    input_voltage=480.0,
    output_voltage=480.0,
    battery_runtime_minutes_at_100pct=15.0,
    efficiency_pct=96.5
)
```
