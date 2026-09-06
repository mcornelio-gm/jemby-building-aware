# Object Specification: Buck-Boost Specialty Autotransformer

## 1. Overview
The **Buck-Boost Specialty Autotransformer** (`BuckBoostTransformerObject`) is an efficient, compact 4-winding insulating transformer connected as an autotransformer to provide small, continuous voltage adjustments ($+5\%\text{ to }+20\%$ boost or $-5\%\text{ to }-20\%$ buck) for specific equipment installations (e.g. boosting $208\text{V}$ line supply to $230\text{V}/240\text{V}$ for European/Canadian motors, or stepping down $240\text{V} \to 208\text{V}$).

* **Class**: `BuckBoostTransformerObject`
* **Parent**: `TransformerObject`
* **Category**: `Specialty Transformer`

---

## 2. Technical Specifications
* **Nameplate Isolated kVA**: Small continuous rating ($0.25\text{ kVA} - 10\text{ kVA}$)
* **Autotransformer Load kVA**: High throughput capacity ($5\text{ kVA} - 100\text{ kVA}+$) due to autotransformer conduction
* **Common Voltage Combinations**:
  * $208\text{V} \to 230\text{V}$ ($+10.58\%$ Boost)
  * $208\text{V} \to 240\text{V}$ ($+15.38\%$ Boost)
  * $240\text{V} \to 208\text{V}$ ($-13.33\%$ Buck)
  * $480\text{V} \to 456\text{V}$ ($-5.0\%$ Buck)

---

## 3. Deterministic Rules & Validation
1. **Voltage Delta Limit**: Asserts that voltage change does not exceed $25\%$ of supply voltage (larger step ratios require full isolation transformers).

---

## 4. Python Example
```python
from james_app.core.transformers import BuckBoostTransformerObject

bb = BuckBoostTransformerObject(
    id="xfmr_bb_pump",
    tag="BB-PUMP1",
    name="Process Pump Voltage Booster",
    kva_rating=5.0,
    autotransformer_load_kva=45.0,
    primary_voltage=208.0,
    secondary_voltage=230.0,
    boost_buck_percentage=10.58
)
```
