# Object Specification: Generic / Placeholder Electrical Object

## 1. Overview
The **Generic Electrical Object** (`GenericElectricalObject`) serves as a polymorphic placeholder in the Digital Twin graph when an electrical element's exact hardware specification, vendor model, or internal circuitry is not yet finalized. It allows engineers to draft topological connections, assign provisional load parameters ($\text{kVA}, \text{kW}, \text{Amps}, \text{Voltage}$), and later seamlessly promote the entity into a concrete class (`PanelboardObject`, `CircuitBreakerObject`, `TransformerObject`, etc.) without losing graph references.

* **Class**: `GenericElectricalObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Placeholder / Generic`

---

## 2. Technical Specifications & Kinds
* **Archetype Kinds (`GenericKind`)**:
  * `LOAD`: Generic electrical load (HVAC, chiller, lighting cluster, receptacle bank).
  * `PANEL`: Future subpanel or distribution enclosure.
  * `SWITCH`: Disconnect switch or manual transfer switch.
  * `SOURCE`: Upstream utility service or backup generator source.
  * `TRANSFORMER`: Dry-type or oil-filled step-down transformer.
  * `MOTOR`: Motor, pump, compressor, or industrial machinery.
  * `CUSTOM`: Unspecified custom equipment or packaged OEM skid.
* **Electrical Parameters**:
  * `voltage`: e.g. `"120V"`, `"208V 3Ø"`, `"480V 3Ø"`.
  * `current_amps`: Operating current in Amps.
  * `power_kva`: Apparent power in kVA.
  * `power_kw`: Real power in kW.
  * `power_factor`: Operating power factor ($0.0 - 1.0$, default $0.90$).
* **Extensible Custom Attributes**: Key-value metadata dictionary for site-specific notes, vendor specs, or preliminary drawings.

---

## 3. Class Promotion Engine
Provides runtime conversion methods to transform placeholder instances into concrete objects:
* `promote_to_panel(total_spaces, mains_amps) -> PanelboardObject`
* `promote_to_breaker(slot_start, poles) -> CircuitBreakerObject`

---

## 4. Multi-View Projections
* **Graphviz DOT**: Renders a distinctive dashed rectangular node (`style="rounded,dashed,filled"`) with category badge and load parameters to visually highlight unfinalized equipment.
* **Native HTML**: Interactive card with dashed border, equipment parameters, and an explicit "Promote Class" interactive action trigger.
* **PlantUML SLD**: Clean `<<placeholder>>` node representation.

---

## 5. Python Example
```python
from james_app.core.generic import GenericElectricalObject, GenericKind

# Create a placeholder for a future chiller unit
future_chiller = GenericElectricalObject(
    id="future_chiller_1",
    tag="CH-1 (FUT)",
    name="Future Chilled Water Compressor",
    generic_kind=GenericKind.MOTOR,
    voltage="480V 3Ø",
    current_amps=120.0,
    power_kva=100.0,
    power_factor=0.88,
    custom_attributes={"vendor": "Trane", "fluid": "R-134a"}
)

# Render placeholder Graphviz DOT
dot_snippet = future_chiller.compile_focused_dot()

# Later: Promote to concrete panel or load
```
