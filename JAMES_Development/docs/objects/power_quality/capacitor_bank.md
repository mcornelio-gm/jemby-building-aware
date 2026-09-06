# Object Specification: Power Factor Correction (PFC) Capacitor Bank

## 1. Overview
The **Power Factor Correction (PFC) Capacitor Bank** (`PowerFactorCapacitorBankObject`) injects leading reactive power ($\text{kVAR}$) to offset lagging inductive motor currents across industrial plants and commercial buildings. It improves total system power factor to $\ge 0.95$, eliminates utility low-PF surcharge penalties, and frees up upstream transformer capacity.

* **Class**: `PowerFactorCapacitorBankObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Power Quality`

---

## 2. Technical Specifications
* **Rated Capacity**: Total reactive power injection in $\text{kVAR}$ ($50 - 1000\text{ kVAR}$).
* **Automatic Stepping Controller**: Multi-stage microprocessor controller that automatically switches capacitor steps in/out based on real-time reactive demand.
* **Detuning Harmonic Reactors**: Iron-core series reactors tuned below the 5th harmonic (e.g. $252\text{ Hz} = 4.2\text{nd harmonic}$) to prevent dangerous harmonic resonance when operating on systems with VFDs.

---

## 3. Python Example
```python
from james_app.core.power_quality import PowerFactorCapacitorBankObject

pfc = PowerFactorCapacitorBankObject(
    id="pfc_main_bus",
    tag="PFC-1",
    name="Main Switchboard Automatic Capacitor Bank",
    rated_kvar=200.0,
    voltage=480.0,
    steps_count=8,
    is_automatic_stepped=True,
    has_detuning_reactors=True
)
```
