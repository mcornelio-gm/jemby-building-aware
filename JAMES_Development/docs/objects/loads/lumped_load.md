# Object Specification: Lumped & Aggregate Electrical Branch Loads

## 1. Overview
The **Lumped Load Object** (`LumpedLoadObject`) models aggregate groups of small branch equipment, such as general convenience receptacle circuits, office lighting zones, commercial kitchen equipment banks, and IT server clusters. It applies **NEC Article 220** demand factors ($\%$) to compute realistic diversified demand power.

* **Class**: `LumpedLoadObject`
* **Parent**: `LoadObject`
* **Category**: `General Branch Load`

---

## 2. Technical Specifications
* **Demand Factor Diversification**:
  $$\text{Diversified kVA} = \text{Connected kVA} \times \left(\frac{\text{Demand Factor \%}}{100}\right)$$
* **Energy Metrics**: Supports physical area tracking ($\text{sq ft}$) and power density calculation ($\text{Watts / sq ft}$).

---

## 3. Python Example
```python
from james_app.core.loads import LumpedLoadObject, LoadType

lighting_zone = LumpedLoadObject(
    id="load_ltg_2f",
    tag="LTG-2F",
    name="2nd Floor Commercial Open Office Lighting",
    load_type=LoadType.LIGHTING,
    voltage=277.0,
    phases=1,
    power_kw=12.0,
    power_kva=13.3,
    area_served_sqft=20000.0,
    watts_per_sqft=0.60,
    demand_factor_pct=100.0
)
```
