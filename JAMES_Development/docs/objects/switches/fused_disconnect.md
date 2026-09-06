# Object Specification: Fused Safety Disconnect Switch

## 1. Overview
The **Heavy Duty Fused Safety Disconnect Switch** (`FusedDisconnectSwitchObject`) integrates a visible-blade mechanical loadbreak disconnect with current-limiting UL Class R, J, T, or L rejection fuse clips. It provides up to **200kA RMS symmetrical** short-circuit current ratings (SCCR) and reliable motor branch overcurrent protection for service entrances, heavy industrial motors (NEC 430), and rooftop HVAC chillers.

* **Class**: `FusedDisconnectSwitchObject`
* **Parent**: `SwitchObject`
* **Category**: `Safety Disconnect`

---

## 2. Technical Specifications
* **Fuse Classifications (`FuseClass`)**:
  * `Class R` (RK1 / RK5): $200\text{kA}$ interrupting rejection fuses ($30\text{A} - 600\text{A}$)
  * `Class J`: Compact, high-speed time-delay fuses ($30\text{A} - 600\text{A}$)
  * `Class T`: Ultra-compact high-interrupting fuses ($30\text{A} - 800\text{A}$)
  * `Class L`: Heavy feeder bolted pressure fuses ($601\text{A} - 6000\text{A}$)
* **Horsepower (HP) Ratings**: Sized for locked-rotor motor starting currents at $240\text{V}$, $480\text{V}$, and $600\text{V}$.
* **Blown Fuse Indicators**: Neon or LED illumination across blown fuse clips for rapid fault isolation.

---

## 3. Deterministic Rules & Validation
1. **Fuse Sizing vs Switch Frame**: Validates `fuse_amps <= rated_amps`. Flags an error if installed fuse rating exceeds the continuous switchblade rating.

---

## 4. Python Example
```python
from james_app.core.switches import FusedDisconnectSwitchObject, FuseClass, EnclosureNemaType

fused_sw = FusedDisconnectSwitchObject(
    id="disc_chiller_1",
    tag="DS-CH1",
    name="Rooftop Chiller #1 Fused Disconnect",
    poles=3,
    rated_amps=200,
    fuse_amps=175,
    fuse_class=FuseClass.CLASS_J,
    short_circuit_rating_ka=200.0,
    horsepower_rating_hp=125.0,
    enclosure_type=EnclosureNemaType.NEMA_3R
)
```
