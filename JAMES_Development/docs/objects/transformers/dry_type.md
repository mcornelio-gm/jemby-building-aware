# Object Specification: Dry-Type Step-Down Transformer

## 1. Overview
The **General Purpose Dry-Type Step-Down Transformer** (`DryTypeStepDownTransformerObject`) is an indoor air-cooled distribution transformer engineered to step commercial building power from $480\text{V } 3\text{Ø}$ down to $208\text{Y}/120\text{V } 3\text{Ø } 4\text{W}$ (or $480\text{V} \to 120/240\text{V } 1\text{Ø}$) for tenant lighting, office receptacles, and appliance branch circuits. It features ventilated NEMA 1/3R enclosures, DOE 2016 energy conservation efficiency, and $220^\circ\text{C}$ insulation class.

* **Class**: `DryTypeStepDownTransformerObject`
* **Parent**: `TransformerObject`
* **Category**: `Distribution Transformer`

---

## 2. Technical Specifications
* **Standard Capacities**: $15, 30, 45, 75, 112.5, 150, 225, 300, 500\text{ kVA}$
* **Temperature Rise Ratings**: $150^\circ\text{C}$ (standard), $115^\circ\text{C}$, or $80^\circ\text{C}$ (energy efficient low-loss)
* **Winding Materials**: Aluminum (standard) or Copper (optional high-conductivity)
* **Audible Sound Level**: $45\text{ dBA} - 55\text{ dBA}$ per NEMA ST-20
* **Shielding**: Optional copper foil electrostatic shield between primary and secondary windings
* **Efficiency Standard**: Compliant with DOE 2016 10 CFR Part 431 efficiency levels

---

## 3. Deterministic Rules & Validation
1. **Temperature Rise Check**: Validates standard temperature rise ratings ($80^\circ\text{C}, 115^\circ\text{C}, 150^\circ\text{C}$).
2. **Impedance Range**: Validates $\%Z$ between $3.0\%$ and $6.0\%$.

---

## 4. Python Example
```python
from james_app.core.transformers import DryTypeStepDownTransformerObject

dry_xfmr = DryTypeStepDownTransformerObject(
    id="xfmr_lp1",
    tag="T-LP1",
    name="Lighting Panel Transformer",
    kva_rating=45.0,
    primary_voltage=480.0,
    secondary_voltage=208.0,
    secondary_neutral_voltage=120.0,
    temperature_rise_c=115,
    winding_material="Copper",
    has_electrostatic_shield=True
)
```
