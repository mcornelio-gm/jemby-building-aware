# Object Specification: Liquid-Filled Padmounted Substation Transformer

## 1. Overview
The **Liquid-Filled Padmounted Substation Transformer** (`LiquidFilledPadmountTransformerObject`) is an outdoor, tamper-resistant compartmental step-down transformer designed to transform medium-voltage utility distribution ($13.8\text{kV}, 12.47\text{kV}, 4.16\text{kV}$) down to low-voltage building service entrance distribution ($480\text{Y}/277\text{V}$ or $208\text{Y}/120\text{V}$) for industrial plants, commercial campuses, and data centers ($500\text{ kVA} - 5000\text{ kVA}$).

* **Class**: `LiquidFilledPadmountTransformerObject`
* **Parent**: `TransformerObject`
* **Category**: `Substation Transformer`

---

## 2. Technical Specifications
* **Capacities**: $500, 750, 1000, 1500, 2000, 2500, 3750, 5000\text{ kVA}$
* **Primary Voltages**: Medium-voltage ($4160\text{V}, 12470\text{V}, 13200\text{V}, 13800\text{V}, 34500\text{V}$)
* **Secondary Voltages**: $480\text{Y}/277\text{V}$ or $208\text{Y}/120\text{V } 3\text{Ø } 4\text{W}$
* **Dielectric Insulating Fluid**:
  * `FR3 / Envirotemp`: Less-flammable natural seed ester fluid ($>300^\circ\text{C}$ fire point per NEC 450.23).
  * `Mineral Oil`: Standard petroleum-based dielectric fluid.
* **Overcurrent & Protection**: Primary Bay-O-Net current-sensing fuses with internal isolation links.
* **Front Construction**: Dead-front construction with loadbreak/deadbreak separable elbow connectors.

---

## 3. Deterministic Rules & Validation
1. **Primary Voltage Threshold**: Validates that primary voltage is medium-voltage ($>1000\text{V}$).
2. **Minimum Sizing**: Flags units $<300\text{ kVA}$ (recommending dry-type for smaller loads).

---

## 4. Python Example
```python
from james_app.core.transformers import LiquidFilledPadmountTransformerObject

padmount = LiquidFilledPadmountTransformerObject(
    id="xfmr_sub1",
    tag="PMTR-1",
    name="Campus Utility Service Substation",
    kva_rating=1500.0,
    primary_voltage=12470.0,
    secondary_voltage=480.0,
    secondary_neutral_voltage=277.0,
    dielectric_fluid="FR3 (Less-Flammable Seed Oil)",
    is_dead_front=True,
    has_bayonet_fusing=True
)
```
