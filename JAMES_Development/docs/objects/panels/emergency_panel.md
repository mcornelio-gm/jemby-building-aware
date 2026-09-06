# Object Specification: Emergency & Life Safety Panel (EP)

## 1. Overview
The **Emergency & Life Safety Panelboard** provides dedicated, isolated power to essential life-safety infrastructure (egress emergency lighting, exit signs, fire alarm panels, stairwell pressurization fans, smoke evacuation dampers, and medical critical loads).

* **Class**: `EmergencyPanelObject`
* **Parent**: `PanelboardObject`
* **Category**: `Emergency & Life Safety`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `120/208V 3Ø 4W` or `277/480V 3Ø 4W`
* **Bus Continuous Ampacity**: `100A`, `225A`, `400A`
* **Power Source**: Fed exclusively through an **Automatic Transfer Switch (ATS)** connected to an emergency diesel/gas generator or central battery/UPS system.
* **Standard Space Counts**: `18`, `30`, `42` spaces

---

## 3. NEC Compliance & Segregation Rules
1. **NEC 700 / 701 Segregation**: Emergency circuits must be wired in completely separate raceways, junction boxes, and panelboards from normal utility power.
2. **Upstream Source Validation**: System triggers a warning if the panel is not connected to a designated ATS (`ats_source_id`) or standby generator source.
3. **Emergency Circuit Tagging**: Breakers are visually branded with `[EMERG]` in all schedule and DOT projections.

---

## 4. Python Example
```python
from james_app.core.panels import EmergencyPanelObject

ep = EmergencyPanelObject.create_empty(
    panel_id="EP_1",
    tag="EP-1",
    name="Emergency Life Safety Panel",
    total_spaces=30,
    mains_rating_amps=225
)
ep.ats_source_id = "ATS_1"

# Add life safety egress lighting circuit
ep.add_emergency_circuit(slot_start=1, description="Stairwell Egress Fixtures", amps=20, poles=1)
```
