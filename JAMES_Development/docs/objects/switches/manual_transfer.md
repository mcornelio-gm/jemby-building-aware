# Object Specification: Manual Transfer Switch (MTS)

## 1. Overview
The **Manual Transfer Switch (MTS)** (`ManualTransferSwitchObject`) is a mechanically interlocked double-throw safety switch engineered for manual transfer of building electrical loads between utility power and a portable generator, mobile transformer trailer, or secondary service entrance. A physical interlock prevents concurrent closure of both sources, eliminating dangerous utility backfeeding risks.

* **Class**: `ManualTransferSwitchObject`
* **Parent**: `SwitchObject`
* **Category**: `Transfer Switch`

---

## 2. Technical Specifications
* **Switch Mechanism**: 3-Position Center-OFF Double Throw (`NORMAL - OFF - EMERGENCY`).
* **Quick-Connect Inlets**: Optional Series 16 Color-Coded Cam-Lock mechanical power inlets for rapid portable generator hookup at loading docks or outdoor pads.
* **Standard Ratings**: $100\text{A}, 200\text{A}, 400\text{A}, 600\text{A}, 800\text{A}, 1200\text{A}$.

---

## 3. Python Example
```python
from james_app.core.switches import ManualTransferSwitchObject, ConnectedSource

mts = ManualTransferSwitchObject(
    id="mts_dock",
    tag="MTS-1",
    name="Loading Dock Portable Generator Connection Switch",
    poles=3,
    rated_amps=400,
    voltage=480.0,
    normal_source_id="MDP-1",
    emergency_source_id="PORTABLE_GEN_1",
    active_source=ConnectedSource.NORMAL,
    has_cam_lock_inlet=True
)
```
