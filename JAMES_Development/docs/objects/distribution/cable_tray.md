# Object Specification: Cable Tray Support System (NEC 392)

## 1. Overview
The **Cable Tray System Object** (`CableTrayObject`) represents continuous structural support systems for power, control, instrumentation, and telecom cables per **NEC Article 392**. It models physical width, loading depth, cross-sectional area, and cable fill percentage verification ($\le 50\%$ limit for multi-conductor control, single-layer for large power feeders).

* **Class**: `CableTrayObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Raceway System`

---

## 2. Technical Specifications
* **Tray Types (`CableTrayType`)**:
  * `Ladder`: Maximum conductor ampacity ventilation.
  * `Ventilated Trough`: Perforated bottom.
  * `Solid Bottom`: Shielding against electromagnetic interference (EMI).
  * `Wire Mesh Basket`: Lightweight routing for data and communication cables.
* **Dimensions**: Widths ($6\text{ in} - 48\text{ in}$), Depths ($4\text{ in}, 6\text{ in}$).

---

## 3. Python Example
```python
from james_app.core.distribution import CableTrayObject, CableTrayType

tray = CableTrayObject(
    id="tray_main_feeder",
    tag="TRAY-1",
    name="Main Electrical Room Feeder Cable Tray",
    tray_type=CableTrayType.LADDER,
    width_inches=30.0,
    depth_inches=6.0,
    length_ft=120.0,
    current_fill_pct=42.0
)
```
