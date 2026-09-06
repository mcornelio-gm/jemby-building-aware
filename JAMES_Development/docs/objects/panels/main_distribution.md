# Object Specification: Main Distribution Panel (MDP / Power Panel)

## 1. Overview
The **Main Distribution Panel (MDP)** (or Power Panel, e.g. Square D I-Line, Siemens CDP, Eaton PRL4) serves as the primary electrical distribution hub directly downstream of the utility service entrance or main step-down transformer. It is engineered to distribute bulk 3-phase power to subpanels, transformers, and large mechanical loads.

* **Class**: `MainDistributionPanelObject`
* **Parent**: `PanelboardObject`
* **Category**: `Main Power Distribution`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `277/480V 3Ø 4W` or `120/208V 3Ø 4W`
* **Bus Continuous Ampacity**: `800A`, `1200A`, `1600A`, `2000A`
* **Short-Circuit Rating (SCCR)**: `35kA`, `65kA`, `100kA`
* **Mains Type**: `MCB` (Main Circuit Breaker) or `MLO` (Main Lugs Only)
* **Standard Space Counts**: `30`, `42`, `54`, `72` spaces

---

## 3. Physical Layout & Breaker Matching
* **Matched Breaker Type**: `MoldedCaseBreakerObject` (MCCB).
* **Feeder Configuration**: Predominantly **3-Pole** circuit breakers ($70\text{A} - 800\text{A}$) mounted across Phase A-B-C bus stabs.
* **Cell Spanning**: 3-pole feeders span 3 vertical rows (`ROWSPAN="3"`) in Graphviz and HTML tables.

---

## 4. Deterministic Rules & Validation
1. **Feeder Protection**: Warns if small single-pole branch circuits ($<30\text{A}$) are placed on an MDP (reserved for bulk feeders).
2. **Phase Load Balancing**: Calculates total volt-amperes across Phase A, B, and C. Warns if unbalance exceeds $15\%$.
3. **Bus Continuous Sizing**: Busbar ampacity must be greater than or equal to the main disconnect rating.

---

## 5. Python Example
```python
from james_app.core.panels import MainDistributionPanelObject, SystemType

mdp = MainDistributionPanelObject.create_empty(
    panel_id="MDP_1",
    tag="MDP-1",
    name="Main Power Distribution Panel",
    total_spaces=42,
    mains_rating_amps=800,
    system_type=SystemType.THREE_PHASE_480Y_277V
)

# Add 3-pole feeder to downstream Lighting Panel LP-1
mdp.add_feeder_breaker(slot_start=1, amps=225, target_panel_name="Panelboard LP-1", target_panel_id="LP_1")
```
