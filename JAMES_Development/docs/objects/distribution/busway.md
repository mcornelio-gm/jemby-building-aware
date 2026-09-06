# Object Specification: Busway / Busduct Distribution Trunk

## 1. Overview
The **Busway / Busduct Object** (`BuswayObject`) models prefabricated electrical conductor trunking containing insulated copper or aluminum sandwich busbars. It provides high-capacity power distribution ($800\text{A} - 5000\text{A}$) for vertical high-rise riser shafts and industrial manufacturing plants with integrated plug-in tap-off outlets along the length of the run.

* **Class**: `BuswayObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Busway Infrastructure`

---

## 2. Technical Specifications
* **Busway Types (`BuswayType`)**:
  * `FEEDER`: Solid enclosed trunking for high-amp feeder runs with no intermediate tap openings.
  * `PLUG_IN`: Features regular tap-off plug openings for quick attachment of branch disconnects.
* **Conductor Materials**: Copper ($1000\text{ A/sq in}$) or Aluminum.
* **Continuous Ampacity**: $800\text{A}, 1000\text{A}, 1200\text{A}, 1600\text{A}, 2000\text{A}, 3000\text{A}, 4000\text{A}, 5000\text{A}$.
* **Short-Circuit Withstand**: $65\text{ kA} - 200\text{ kA}$ RMS symmetrical.

---

## 3. Python Example
```python
from james_app.core.distribution import BuswayObject, BuswayType, BuswayConductorMaterial

busway = BuswayObject(
    id="busway_riser_1",
    tag="BUSWAY-1",
    name="East Tower Electrical Riser Busway",
    busway_type=BuswayType.PLUG_IN,
    conductor_material=BuswayConductorMaterial.COPPER,
    rated_amps=2000,
    voltage=480.0,
    length_ft=150.0,
    plug_in_outlets_count=12
)
```
