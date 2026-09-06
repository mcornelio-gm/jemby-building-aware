# Object Specification: Panelboard (Base Enclosure Object)

## 1. Overview
The **Panelboard** base class (`PanelboardObject`) models standard electrical distribution enclosures containing busbars, neutral/ground assemblies, overcurrent protective devices (circuit breakers), and incoming service lugs. It encapsulates physical slot layout geometry, bus phase alternating mechanics, deterministic sizing algorithms, and multi-view rendering projections.

* **Class**: `PanelboardObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Distribution Enclosure`

---

## 2. Electrical & Geometric Attributes
* **System Types**:
  * `THREE_PHASE_208Y_120V`: $120/208\text{V } 3\text{Ø } 4\text{W}$
  * `THREE_PHASE_480Y_277V`: $277/480\text{V } 3\text{Ø } 4\text{W}$
  * `SINGLE_PHASE_120_240V`: $120/240\text{V } 1\text{Ø } 3\text{W}$
* **Mains Types**: `MCB` (Main Circuit Breaker) or `MLO` (Main Lugs Only)
* **Standard Space Counts**: $18, 30, 42, 54, 72, 84$ physical slots
* **Bus Continuous Ampacity**: $100\text{A}, 225\text{A}, 400\text{A}, 600\text{A}, 800\text{A}, 1200\text{A}+$

---

## 3. Bus Phase Alternation Mechanics
Phase stabs are indexed mathematically by physical slot number:
* **3-Phase Panelboards**:
  * Row 0 (Slots 1 & 2): **Phase A**
  * Row 1 (Slots 3 & 4): **Phase B**
  * Row 2 (Slots 5 & 6): **Phase C**
  * Row 3 (Slots 7 & 8): **Phase A** (repeats modulo 3)
* **1-Phase Panelboards**:
  * Row 0 (Slots 1 & 2): **Phase A**
  * Row 1 (Slots 3 & 4): **Phase B**
  * Row 2 (Slots 5 & 6): **Phase A** (repeats modulo 2)

---

## 4. Multi-Pole Slot Spanning & Layout Rules
* A breaker starting at `slot_start` with `poles` poles occupies slots:
  $$\text{occupied\_slots} = [\text{slot\_start} + 2i \quad \text{for } i \in \{0, \dots, \text{poles}-1\}]$$
* **Table Span Rendering**:
  * The description cell uses `ROWSPAN="poles"`.
  * Physical slot numbers ($1, 2, 3, \dots$) are emitted on every row to preserve grid structure and terminal ports.
* **Auto-Sizing Rule**: Sizing algorithm finds smallest standard enclosure count such that:
  $$\text{total\_spaces} \ge \text{poles\_used} \times 1.20 \quad (\ge 20\% \text{ spare capacity})$$

---

## 5. Multi-View Visual Projections
1. **Graphviz DOT**: 4-column HTML table with `ROWSPAN` spanning, color-coded status badges, and cell-level port handles (`ckt_1_3_5`).
2. **Native HTML/Tailwind**: Modern responsive schedule component with dark mode, interactive hover states, and slot badges.
3. **PlantUML SLD**: Clean single-line diagram with busbar enclosure and downstream branch feeds.
4. **Gemini AI Context**: Full structured serialization (`to_gemini_context()`) for automated prompt ingestion.

---

## 6. Python Example
```python
from james_app.core.panels import PanelboardObject, SystemType, MainsType

# Instantiate an empty 42-space panelboard
panel = PanelboardObject.create_empty(
    panel_id="LP_1",
    tag="LP-1",
    name="Lighting & Receptacle Panel",
    total_spaces=42,
    mains_rating_amps=225,
    system_type=SystemType.THREE_PHASE_208Y_120V,
    mains_type=MainsType.MCB
)

# Add 1-Pole, 2-Pole, and 3-Pole branch breakers
panel.add_breaker(slot_start=1, poles=1, amps=20, description="Hallway Lighting")
panel.add_breaker(slot_start=2, poles=2, amps=30, description="Server Room AC Unit")
panel.add_breaker(slot_start=5, poles=3, amps=60, description="Rooftop Exhaust Fan")

# Evaluate rules and render projections
warnings = panel.validate_rules()
dot_graph = panel.compile_focused_dot()
html_table = panel.render_html_view()
puml_sld = panel.compile_plantuml_sld()
```
