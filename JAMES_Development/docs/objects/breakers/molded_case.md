# Object Specification: Molded Case Circuit Breaker (MCCB)

## 1. Overview
The **Molded Case Circuit Breaker (MCCB)** (`MoldedCaseBreakerObject`) is an industrial-grade overcurrent and short-circuit protective device designed for high-amperage feeder distribution, main service disconnects, and industrial equipment feeds ($70\text{A} - 800\text{A}+$ with up to $100\text{kA}$ interrupting capacity). It supports interchangeable thermal-magnetic or solid-state Electronic Trip Units (ETU / Micrologic).

* **Class**: `MoldedCaseBreakerObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **Frame Sizes**:
  * `H-Frame`: Up to $150\text{A}$
  * `J-Frame`: Up to $250\text{A}$
  * `L-Frame`: Up to $400\text{A}$
  * `P-Frame`: Up to $800\text{A}$
  * `R-Frame`: Up to $1600\text{A}+$
* **Interrupting Rating ($\text{AIC}$)**: $22\text{kA}$, $35\text{kA}$, $65\text{kA}$, $100\text{kA}$ @ $480\text{V}$
* **Trip Unit Technology**: Thermal-Magnetic or Electronic Trip Unit (ETU / Micrologic) with adjustable long-time, short-time, and instantaneous trip curves.
* **Compatible Enclosures**: `MainDistributionPanelObject` (MDP / I-Line / CDP), `MotorControlCenterObject`, heavy Switchboards.

---

## 3. Physical Layout & Multi-Pole Spanning
* Predominantly **3-Pole** ($3\text{Ø}$) or **2-Pole** configurations spanning consecutive phase stabs.
* Spans 2 or 3 vertical rows (`ROWSPAN="2"` or `ROWSPAN="3"`) in Graphviz DOT and HTML panel schedules.

---

## 4. Deterministic Rules & Validation
1. **Frame Sizing Check**: Trip rating (`amps`) must not exceed physical frame ampacity (`frame_amps`).
2. **Panel Compatibility Rule**: Warns if installed on small lighting branch panels or residential loadcenters not engineered for MCCB mechanical stab depths.

---

## 5. Python Example
```python
from james_app.core.breakers import MoldedCaseBreakerObject, BreakerStatus

mccb = MoldedCaseBreakerObject(
    id="bkr_mdp1_1",
    tag="CB-1/3/5",
    name="Feeder to Subpanel LP-1",
    slot_start=1,
    poles=3,
    occupied_slots=[1, 3, 5],
    amps=225,
    frame_amps=250,
    frame_name="J-Frame (250A)",
    aic_rating_ka=65.0,
    has_electronic_trip=True,
    status=BreakerStatus.ON,
    connected_phases=["A", "B", "C"]
)
```
