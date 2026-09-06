# Object Specification: Electric Motor (Rotating Machinery)

## 1. Overview
The **Electric Motor Object** (`ElectricMotorObject`) models 3-phase and 1-phase AC induction and synchronous electric motors per **NEC Article 430**. It calculates standard NEC Table 430.250 Full Load Amps (FLA), locked-rotor starting current (LRA), branch circuit conductor sizing ($125\%$ FLA per NEC 430.22), and maximum inverse-time breaker sizing ($250\%$ FLA per NEC 430.52).

* **Class**: `ElectricMotorObject`
* **Parent**: `LoadObject`
* **Category**: `Rotating Machinery`

---

## 2. Technical Specifications & NEC 430 Formulas
* **Horsepower (HP)**: $1.0\text{ HP} - 500\text{ HP}+$
* **NEC Table 430.250 FLA**: Standard full-load currents (e.g. $25\text{ HP @ 460V} = 34\text{ A}$, $50\text{ HP @ 460V} = 65\text{ A}$).
* **Branch Conductor Sizing (NEC 430.22)**:
  $$\text{Conductor Ampacity} \ge 125\% \times \text{NEC Table FLA}$$
* **Inverse-Time Breaker OCPD Sizing (NEC 430.52)**:
  $$\text{Max Breaker Rating} \le 250\% \times \text{NEC Table FLA}$$
* **Locked Rotor Current (LRA)**: $\approx 6 \times \text{FLA}$ (NEMA Code Letter G).

---

## 3. Python Example
```python
from james_app.core.loads import ElectricMotorObject

motor = ElectricMotorObject(
    id="load_pump_1",
    tag="MTR-PUMP1",
    name="Chilled Water Supply Pump Motor",
    horsepower_hp=50.0,
    voltage=480.0,
    phases=3,
    rpm=1750
)
# Calculations:
# NEC Table FLA: 65.0 A
# Conductor Ampacity (125%): 81.25 A
# Max Breaker (250%): 162.5 A
```
