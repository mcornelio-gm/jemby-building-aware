# Object Specification: Motor Circuit Protector (MCP)

## 1. Overview
The **Motor Circuit Protector (MCP / Instantaneous-Trip Breaker)** (`MotorCircuitProtectorObject`) is an instantaneous-magnetic-only circuit breaker engineered specifically for combination motor starters within Motor Control Centers (MCCs) and industrial machine panels per **NEC 430.52**. It omits internal thermal overload bimetals, delegating thermal protection to downstream solid-state or bimetallic overload relays (OLRs) or Variable Frequency Drives (VFDs).

* **Class**: `MotorCircuitProtectorObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **Trip Mechanism**: Instantaneous Magnetic Only (No thermal element).
* **Adjustable Magnetic Setting**: $300\text{A} - 3500\text{A}$ (typically calibrated to $700\% - 1300\%$ of Motor Full Load Amps / FLA).
* **Poles**: 3-Pole ($3\text{Ø}$) standard for commercial/industrial motors.
* **Interrupting Rating ($\text{AIC}$)**: $35\text{kA}, 65\text{kA}, 100\text{kA}$.
* **Compatible Enclosures**: `MotorControlCenterObject` (MCC), Industrial Machine Control Enclosures.

---

## 3. Deterministic Rules & Validation
1. **3-Pole Rule**: Industrial MCPs in 3-phase MCCs must be 3-pole devices. Flags a warning if configured with 1 or 2 poles.
2. **Combination Requirement**: Requires association with downstream thermal overload relay or VFD starter assembly.

---

## 4. Python Example
```python
from james_app.core.breakers import MotorCircuitProtectorObject, BreakerStatus

mcp = MotorCircuitProtectorObject(
    id="bkr_mcc1_1",
    tag="MCP-1",
    name="Chilled Water Pump #1 Starter Feed",
    slot_start=1,
    poles=3,
    occupied_slots=[1, 3, 5],
    amps=100,
    magnetic_trip_setting_amps=1100.0,
    status=BreakerStatus.ON,
    connected_phases=["A", "B", "C"]
)
```
