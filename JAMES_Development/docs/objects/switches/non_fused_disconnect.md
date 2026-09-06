# Object Specification: Non-Fused Safety Disconnect Switch

## 1. Overview
The **Non-Fused Safety Disconnect Switch** (`NonFusedDisconnectSwitchObject`) provides a visible-blade or rotary mechanical air-gap isolation point directly within sight of electric motors (NEC 430.102), HVAC equipment (NEC 440.14), pumps, and machinery. It contains no internal fuses, serving strictly as an OSHA-compliant lockable isolation apparatus while relying on upstream panel circuit breakers for overcurrent and short-circuit protection.

* **Class**: `NonFusedDisconnectSwitchObject`
* **Parent**: `SwitchObject`
* **Category**: `Safety Disconnect`

---

## 2. Technical Specifications
* **Standard Ratings**: $30\text{A}, 60\text{A}, 100\text{A}, 200\text{A}, 400\text{A}, 600\text{A}, 800\text{A}, 1200\text{A}$
* **Operating Styles**: Side-mount heavy duty knife blade handle or front-mount rotary door disconnect.
* **Short-Circuit Rating (SCCR)**: Base $10\text{kA}$ withstand, upgradable to $100\text{kA} - 200\text{kA}$ when series-rated with upstream current-limiting fuses or circuit breakers.
* **Lockout/Tagout**: Accepts up to 3 padlocks in the OPEN position per OSHA 1910.147.

---

## 3. Deterministic Rules & Validation
1. **Within-Sight Distance Rule**: Asserts that the disconnect is located within 50 feet and visible from the driven machine per **NEC 430.102**.

---

## 4. Python Example
```python
from james_app.core.switches import NonFusedDisconnectSwitchObject, EnclosureNemaType

non_fused = NonFusedDisconnectSwitchObject(
    id="disc_ahu1",
    tag="DS-AHU1",
    name="Air Handling Unit AHU-1 Local Disconnect",
    poles=3,
    rated_amps=60,
    voltage=480.0,
    is_within_sight=True,
    enclosure_type=EnclosureNemaType.NEMA_1
)
```
