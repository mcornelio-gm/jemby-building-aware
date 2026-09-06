# Object Specification: Transformer (Base Transformation Object)

## 1. Overview
The **Transformer** base class (`TransformerObject`) represents electromagnetic inductive apparatus designed to step voltage up or down between transmission, distribution, and utilization levels ($480\text{V} \to 208\text{Y}/120\text{V}$, $12.47\text{kV} \to 480\text{V}$, etc.). It implements deterministic full-load current (FLA) physics, secondary available short-circuit current calculations ($I_{sc}$), NEC 450 overcurrent protection sizing rules, standard kVA steps, and multi-view rendering projections.

* **Class**: `TransformerObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Transformer`

---

## 2. Electrical Specifications & Standard Sizing
* **Standard kVA Steps (`STANDARD_KVA_RATINGS`)**:
  $$15, 30, 45, 75, 112.5, 150, 225, 300, 500, 750, 1000, 1500, 2000, 2500, 3750, 5000\text{ kVA}$$
* **Winding Configurations (`WindingConfiguration`)**:
  * `DELTA_WYE`: Delta primary ($3\text{W}$) with Wye secondary ($4\text{W}$ with grounded neutral $X_0$).
  * `DELTA_DELTA`: Delta-to-Delta ($3\text{W}$).
  * `WYE_WYE`: Wye-to-Wye ($4\text{W}$).
  * `SINGLE_PHASE`: $1\text{Ø}$ 2-wire / 3-wire ($120/240\text{V}$).
* **Cooling Types (`CoolingType`)**: `ANN_AIR` (Dry-Type Ventilated), `AF_FORCED_AIR`, `ONAN_OIL` (Mineral Oil), `KNAN_LESS_FLAMMABLE` (FR3 Seed Oil).
* **Percent Impedance ($\%Z$)**: Nameplate impedance (typically $2.0\% - 5.75\%$).

---

## 3. Deterministic Physics & Formulas

### Full-Load Current Calculations (FLA)
* **Three-Phase ($3\text{Ø}$)**:
  $$I_{\text{FLA}} = \frac{\text{kVA} \times 1000}{\sqrt{3} \times V_{\text{line-to-line}}}$$
* **Single-Phase ($1\text{Ø}$)**:
  $$I_{\text{FLA}} = \frac{\text{kVA} \times 1000}{V_{\text{nominal}}}$$

### Maximum Available Secondary Fault Current ($I_{sc}$)
$$I_{sc} = \frac{I_{\text{sec\_FLA}}}{\%Z / 100}$$

### NEC 450.3(B) Maximum OCPD Protection Sizing
* Primary OCPD with secondary protection ($\le 125\%$): Max Primary = $250\% \times I_{\text{pri\_FLA}}$.
* Primary OCPD only (without secondary protection): Max Primary = $125\% \times I_{\text{pri\_FLA}}$.

---

## 4. Connectivity Terminals
* **Primary Inputs (`get_input_ports`)**: `["H1", "H2", "H3", "GND"]` (or `["H1", "H2"]` for $1\text{Ø}$).
* **Secondary Outputs (`get_output_ports`)**: `["X1", "X2", "X3", "X0", "GND"]` for Delta-Wye.

---

## 5. Python Example
```python
from james_app.core.transformers import TransformerObject, WindingConfiguration

xfmr = TransformerObject(
    id="xfmr_t1",
    tag="T-1",
    name="Building 480V to 208Y/120V Step-Down Transformer",
    kva_rating=75.0,
    primary_voltage=480.0,
    secondary_voltage=208.0,
    secondary_neutral_voltage=120.0,
    winding_config=WindingConfiguration.DELTA_WYE,
    impedance_pct_z=5.0
)

# Deterministic calculations:
# Primary FLA: 90.21 A
# Secondary FLA: 208.18 A
# Available Secondary I_sc: 4,164 A
```
