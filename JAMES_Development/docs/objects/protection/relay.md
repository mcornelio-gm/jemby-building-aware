# Object Specification: Microprocessor Numerical Protective Relay

## 1. Overview
The **Protective Relay Object** (`ProtectiveRelayObject`) models modern numerical microprocessor protection relays (e.g. SEL, GE Multilin, Schneider Sepam, ABB Relion). It coordinates with upstream current and voltage transformers to execute selective tripping, arc-flash mitigation ($<2\text{ms}$ optical detection), and standard IEEE/ANSI device protection functions.

* **Class**: `ProtectiveRelayObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Protective Relaying`

---

## 2. Standard IEEE / ANSI Protection Functions
* **50 / 51**: Instantaneous & Time-Overcurrent Phase Protection
* **50N / 51N / 50G**: Ground Fault Time & Instantaneous Overcurrent
* **87**: High-Speed Differential Protection (Transformer / Generator / Bus)
* **27 / 59**: Under-Voltage & Over-Voltage Protection
* **81O / 81U**: Over-Frequency & Under-Frequency Protection
* **32**: Directional Reverse Power Protection (Generator Anti-Motoring)
* **67**: Directional Phase Overcurrent

---

## 3. Python Example
```python
from james_app.core.protection import ProtectiveRelayObject

relay = ProtectiveRelayObject(
    id="relay_main_52m",
    tag="RELAY-52M",
    name="Main Service Entrance Feeder Relay",
    relay_model="SEL-751",
    ansi_functions=["50/51", "50N/51N", "27/59", "81O/U"],
    trip_curve_type="IEEE Very Inverse (U3)",
    pickup_current_amps=5.0,
    time_dial_setting=2.5,
    controls_breaker_id="MAIN-SWG-1"
)
```
