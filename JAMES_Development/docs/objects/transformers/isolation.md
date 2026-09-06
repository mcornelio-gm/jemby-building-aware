# Object Specification: Precision Isolation Transformer

## 1. Overview
The **Precision Isolation Transformer** (`IsolationTransformerObject`) provides electrical and galvanic isolation between primary distribution feeds and sensitive downstream critical electronics (data centers, broadcast studios, PLC controls) or hospital wet procedure and operating rooms per **NEC 517**. It establishes a new separately derived system (SDS) with zero ground loops, dual copper electrostatic Faraday shields, and harmonic non-linear load handling ($K\text{-Factor } 13 / 20$).

* **Class**: `IsolationTransformerObject`
* **Parent**: `TransformerObject`
* **Category**: `Clean Power Equipment`

---

## 2. Technical Specifications
* **Harmonic Rating ($K\text{-Factor}$)**: $K\text{-13}$ or $K\text{-20}$ for server power supplies and switch-mode converter harmonics.
* **Common-Mode Noise Attenuation**: Up to $120\text{ dB}$ ($0.001\text{ pF}$ effective capacitance).
* **Transverse-Mode Noise Attenuation**: Up to $30\text{ dB}$.
* **Shielding**: Dual continuous copper electrostatic shields between primary and secondary windings.
* **Standard Capacities**: $15, 30, 50, 75, 100, 150, 225\text{ kVA}$.

---

## 3. Deterministic Rules & Validation
1. **Harmonic K-Factor Check**: IT and clean power isolation transformers recommend $K\text{-Factor} \ge 4$ (standard $K\text{-13}$).
2. **Medical SDS Verification**: When flagged for healthcare wet procedure locations, validates compatibility with ungrounded isolated power systems and Line Isolation Monitors (LIM).

---

## 4. Python Example
```python
from james_app.core.transformers import IsolationTransformerObject

iso = IsolationTransformerObject(
    id="xfmr_iso_dc",
    tag="ISO-DC-1",
    name="Data Center PDU Isolation Transformer",
    kva_rating=100.0,
    primary_voltage=480.0,
    secondary_voltage=208.0,
    secondary_neutral_voltage=120.0,
    k_factor=13,
    common_mode_attenuation_db=120
)
```
