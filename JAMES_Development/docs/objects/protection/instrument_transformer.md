# Object Specification: Instrument Transformers (CT & PT)

## 1. Overview
The **Instrument Transformer Classes** (`CurrentTransformerObject` and `PotentialTransformerObject`) represent precision stepping apparatus designed to safely isolate and scale down high primary current and voltage signals for protective relays, digital meters, and revenue billing recorders per **IEEE C57.13**.

* **Classes**: `CurrentTransformerObject`, `PotentialTransformerObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Instrument Transformer`

---

## 2. Technical Specifications

### Current Transformer (CT)
* **Primary Ratio**: $200\text{A}, 400\text{A}, 600\text{A}, 800\text{A}, 1200\text{A}, 2000\text{A}, 4000\text{A}$.
* **Secondary Standard**: $5\text{A}$ (North American standard) or $1\text{A}$ (IEC standard).
* **Accuracy & Relaying Class**: Metering accuracy (e.g. $0.3\text{ B-0.5}$) and relaying accuracy class (e.g. $\text{C400}$ / $\text{C800}$).

### Potential Transformer (PT / VT)
* **Primary Voltages**: $480\text{V}, 4160\text{V}, 12470\text{V}, 13800\text{V}$.
* **Secondary Standard**: $120\text{V}$ (or $69.3\text{V}$ line-to-neutral).
* **Accuracy Class**: $0.3\text{ W, X, M, Y, Z}$ ($0.3\%$ revenue metering accuracy).

---

## 3. Python Example
```python
from james_app.core.protection import CurrentTransformerObject, PotentialTransformerObject

ct = CurrentTransformerObject(
    id="ct_phase_a",
    tag="CT-1A",
    name="Main Feeder Phase A Current Transformer",
    primary_ratio_amps=2000,
    secondary_ratio_amps=5,
    accuracy_class="0.3 B-0.5 / C400"
)

pt = PotentialTransformerObject(
    id="pt_bus_1",
    tag="PT-1",
    name="Main Switchgear Bus Potential Transformer",
    primary_voltage=480.0,
    secondary_voltage=120.0
)
```
