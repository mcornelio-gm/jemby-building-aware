# Object Specification: Subpanel / Remote Distribution Panel

## 1. Overview
A **Subpanel** is a secondary electrical panelboard fed from an upstream Main Distribution Panel (MDP), Switchboard, or primary branch panel. It serves localized zone loads (e.g. detached structures, floor tenant suites, mechanical rooms) to reduce home-run conductor lengths and voltage drop.

* **Class**: `SubpanelObject`
* **Parent**: `PanelboardObject`
* **Category**: `Sub-Distribution Panel`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `120/208V 3Ø 4W` or `120/240V 1Ø 3W`
* **Bus Continuous Ampacity**: `60A`, `100A`, `125A`, `200A`, `225A`
* **Mains Type**: Defaults to **Main Lugs Only (MLO)** (overcurrent protection provided by the upstream feeder breaker), or equipped with a local sub-main disconnect.
* **Neutral / Ground Bonding (NEC 250.32)**: Neutral bus must remain floating (insulated from the enclosure); ground bus is bonded directly to the enclosure with a separate equipment grounding conductor (EGC) back to the main service.

---

## 3. Deterministic Rules & Validation
1. **Upstream Feeder Assignment**: Triggers a warning if the subpanel lacks an assigned feeding parent panel or source.
2. **Bus vs Feeder Coordination**: Subpanel bus rating must be equal to or greater than the upstream feeder breaker rating.

---

## 4. Python Example
```python
from james_app.core.panels import SubpanelObject

sub = SubpanelObject.create_empty(
    panel_id="SUB_FLOOR_2",
    tag="PANEL-2A",
    name="2nd Floor West Subpanel",
    total_spaces=24,
    mains_rating_amps=100
)
sub.upstream_panel_id = "MDP_1"
```
