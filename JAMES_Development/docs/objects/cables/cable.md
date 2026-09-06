# Object Specification: Cable & Conductor Run

## 1. Overview
The **Cable / Conductor Run Object** (`CableObject`) models the physical electrical conductors and raceways connecting equipment terminals across the Digital Twin graph (e.g. from an MDP breaker output port to a downstream subpanel input lug). It encapsulates wire gauges, conductor metals, insulation types, conduit raceways, parallel conductor sets, NEC 310.16 ampacity tables, and Ohm's law voltage drop ($V_d$) physics.

* **Class**: `CableObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Conductor Run`

---

## 2. Technical Specifications
* **Conductor Gauges**: `14 AWG` through `4/0 AWG`, and `250 kcmil` through `750 kcmil`.
* **Conductor Materials (`ConductorMaterial`)**: `COPPER` (Cu) or `ALUMINUM` (Al).
* **Insulation Ratings (`InsulationType`)**: `THHN` ($90^\circ\text{C}$ dry), `THWN-2` ($90^\circ\text{C}$ wet/dry), `XHHW-2`, `USE-2`.
* **Raceway / Conduit (`ConduitType`)**: `EMT`, `PVC`, `RMC`, `MC_CABLE`, `FREE_AIR`.
* **Parallel Sets (`sets`)**: Integer multiplier (e.g. $2\times, 3\times, 4\times$ parallel runs).
* **Length (`length_ft`)**: One-way physical circuit distance in feet.
* **Operating Design Current (`load_amps`)**: Real-time or design load in Amps.
* **Nominal Operating Voltage (`nominal_voltage`)**: $120\text{V}, 208\text{V}, 240\text{V}, 277\text{V}, 480\text{V}$.

---

## 3. Deterministic Physics & Calculations

### Ampacity Verification (NEC Table 310.16)
$$\text{Total Ampacity} = \text{Base Ampacity}(75^\circ\text{C}) \times \text{sets}$$

### Voltage Drop Calculation ($V_d$)
* **Single-Phase ($1\text{Ø}$)**:
  $$V_d = \frac{2 \times L \times R \times I}{1000 \times \text{sets}}$$
* **Three-Phase ($3\text{Ø}$)**:
  $$V_d = \frac{\sqrt{3} \times L \times R \times I}{1000 \times \text{sets}}$$
* **Percentage Drop**:
  $$\%V_d = \left( \frac{V_d}{V_{\text{nominal}}} \right) \times 100\%$$

---

## 4. Deterministic Rules & Validation
1. **Ampacity Limit Rule**: Asserts `load_amps <= base_ampacity`. Flags an overload violation warning if current exceeds rated conductor ampacity.
2. **NEC 3% Voltage Drop Rule**: Asserts that total branch/feeder voltage drop does not exceed the NEC recommended maximum of $3.0\%$.

---

## 5. Visual Projections
* **Graphviz DOT**: Renders a directed connection edge with wire count, gauge, material, and length annotations.
* **Native HTML**: Interactive card badge displaying conductor gauge, conduit raceway, length, rated ampacity, and dynamic color-coded voltage drop percentage ($\le 3\%$ green, $>3\%$ red).
* **PlantUML SLD**: Clean schematic connection line with feeder tag and distance annotation.

---

## 6. Python Example
```python
from james_app.core.cable import CableObject, ConductorMaterial, InsulationType, ConduitType

# 200A Feeder Cable from MDP-1 to Subpanel LP-1
feeder_cable = CableObject(
    id="feed_mdp1_lp1",
    tag="FEED-LP1",
    name="MDP-1 to LP-1 Feeder",
    gauge="3/0 AWG",
    material=ConductorMaterial.COPPER,
    insulation=InsulationType.THHN,
    conduit=ConduitType.EMT,
    length_ft=125.0,
    sets=1,
    num_conductors=4,
    from_node_id="Panel_MDP_1",
    from_port_id="ckt_1_3_5",
    to_node_id="Panel_LP_1",
    to_port_id="main",
    load_amps=160.0,
    nominal_voltage=208.0
)

# Evaluate ampacity and voltage drop
warnings = feeder_cable.validate_rules()
vd_stats = feeder_cable.calculate_voltage_drop(is_three_phase=True)
# Result: {'drop_volts': 2.66, 'drop_pct': 1.28, 'max_recommended_pct': 3.0}
```
