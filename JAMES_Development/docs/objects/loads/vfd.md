# Object Specification: Variable Frequency Drive (VFD)

## 1. Overview
The **Variable Frequency Drive (VFD)** (`VariableFrequencyDriveObject`) models solid-state inverter motor speed controllers. It defines input continuous rated current, output variable-frequency current, PWM carrier switching frequencies ($2\text{ kHz} - 16\text{ kHz}$), $3\% / 5\%$ input harmonic line reactors, and optional 3-contactor maintenance bypass configurations.

* **Class**: `VariableFrequencyDriveObject`
* **Parent**: `LoadObject`
* **Category**: `Motor Control`

---

## 2. Technical Specifications
* **Rated Output Current**: Continuous motor driving capacity in Amps.
* **Input Line Reactor**: $3\%$ or $5\%$ impedance reactor for harmonic THD attenuation and transient surge suppression.
* **Carrier Frequency**: PWM switching rate in $\text{kHz}$.
* **Bypass Contactor Option**: 3-contactor scheme (Drive Input, Drive Output, Across-The-Line Bypass).

---

## 3. Python Example
```python
from james_app.core.loads import VariableFrequencyDriveObject

vfd = VariableFrequencyDriveObject(
    id="vfd_fan_1",
    tag="VFD-SF1",
    name="Supply Fan VFD Controller",
    motor_hp=30.0,
    voltage=480.0,
    phases=3,
    rated_input_amps=42.0,
    rated_output_amps=40.0,
    has_input_line_reactor=True
)
```
