# Object Specification: Automatic Transfer Switch (ATS)

## 1. Overview
The **Automatic Transfer Switch (ATS)** (`AutomaticTransferSwitchObject`) is an intelligent critical power apparatus that monitors incoming Normal (Utility) power quality. Upon detecting voltage sag, phase loss, or total outage, it automatically signals an emergency engine-generator to start via dry contacts, waits for generator voltage and frequency stabilization, and transfers critical building loads to the Emergency source per **NEC 700 / 701 / 702**.

* **Class**: `AutomaticTransferSwitchObject`
* **Parent**: `SwitchObject`
* **Category**: `Transfer Switch`

---

## 2. Technical Specifications
* **Dual-Source Architecture**:
  * `normal_source_id`: Upstream Utility feed or MDP.
  * `emergency_source_id`: Backup Diesel/Gas Generator, UPS, or secondary substation.
* **Transition Modes (`TransferTransitionType`)**:
  * `Open Transition`: Standard break-before-make transfer with brief millisecond interruption.
  * `Closed Transition`: Make-before-break soft-load parallel transfer ($<100\text{ms}$) with zero power interruption.
  * `Delayed Transition`: Programmed center-off neutral pause allowing inductive motor back-EMF to decay before reconnection.
* **Control Timers**:
  * Engine Start Delay ($1-10\text{s}$)
  * Transfer Time Delay ($0-60\text{s}$)
  * Retransfer to Utility Delay ($5-30\text{min}$)
  * Generator Unloaded Cool-Down ($5-15\text{min}$)
* **Weekly Engine Exerciser**: Programmable automatic generator test timer with or without load transfer.

---

## 3. Terminal Connectivity
* **Inputs (`get_input_ports`)**: Normal source (`norm_L1`, `norm_L2`, `norm_L3`) and Emergency source (`emerg_L1`, `emerg_L2`, `emerg_L3`).
* **Outputs (`get_output_ports`)**: Common load bus (`load_T1`, `load_T2`, `load_T3`, `load_N`).

---

## 4. Python Example
```python
from james_app.core.switches import (
    AutomaticTransferSwitchObject,
    ConnectedSource,
    TransferTransitionType,
)

ats = AutomaticTransferSwitchObject(
    id="ats_life_safety",
    tag="ATS-LS1",
    name="Life Safety & Egress Lighting ATS",
    poles=4,
    rated_amps=400,
    voltage=480.0,
    normal_source_id="MDP-1",
    emergency_source_id="GEN-1",
    active_source=ConnectedSource.NORMAL,
    transition_type=TransferTransitionType.OPEN_TRANSITION,
    transfer_time_delay_sec=3.0,
    retransfer_time_delay_sec=600.0
)
```
