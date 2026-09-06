# Object Specification: Bypass-Isolation Automatic Transfer Switch

## 1. Overview
The **Bypass-Isolation Automatic Transfer Switch** (`BypassIsolationSwitchObject`) is a dual-mechanism critical power transfer apparatus engineered for healthcare facilities (NFPA 99 / NEC 517), hyperscale data centers, and critical emergency infrastructures. It combines a drawout automatic transfer switch (ATS) with a dedicated manual bypass switch, enabling complete mechanical racking, routine testing, and live contact replacement without dropping power to downstream critical branch loads.

* **Class**: `BypassIsolationSwitchObject`
* **Parent**: `AutomaticTransferSwitchObject`
* **Category**: `Critical Power Transfer Switch`

---

## 2. Technical Specifications
* **Dual Mechanisms**:
  1. **Primary ATS**: Fully automatic drawout racking unit.
  2. **Manual Bypass Switch**: Heavy-duty visible contact switch allowing manual selection of Normal or Emergency feeds directly to the load bus.
* **No-Break Overlap**: Zero-interruption overlapping contacts prevent power glitches during bypass engagement.
* **Standard Ratings**: $100\text{A}, 225\text{A}, 400\text{A}, 800\text{A}, 1200\text{A}, 2000\text{A}, 3000\text{A}, 4000\text{A}$.
* **Compliance**: Meets NFPA 110, NFPA 99 Essential Electrical Systems, and UL 1008.

---

## 3. Python Example
```python
from james_app.core.switches import BypassIsolationSwitchObject, ConnectedSource

bypass_ats = BypassIsolationSwitchObject(
    id="ats_byp_icu",
    tag="ATS-BYP-ICU",
    name="Intensive Care Unit Critical Power ATS",
    poles=4,
    rated_amps=800,
    voltage=480.0,
    normal_source_id="MDP-NORMAL",
    emergency_source_id="GEN-EMERGENCY",
    is_drawout_ats=True,
    has_zero_interruption_transfer=True
)
```
