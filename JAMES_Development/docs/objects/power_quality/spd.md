# Object Specification: Surge Protective Device (SPD / TVSS)

## 1. Overview
The **Surge Protective Device (SPD / TVSS)** (`SurgeProtectiveDeviceObject`) protects electrical distribution panels, sensitive electronics, and computer equipment against lightning strikes and high-energy transient voltage surges per **NEC Article 242** and **UL 1449 4th Edition**.

* **Class**: `SurgeProtectiveDeviceObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Surge Protection`

---

## 2. Technical Specifications
* **SPD Types (`SpdType`)**:
  * `Type 1`: Permanently connected on the line or load side of the main service entrance disconnect.
  * `Type 2`: Connected on the load side of the service panel overcurrent device.
  * `Type 3`: Point-of-utilization surge protection (receptacle level).
* **Surge Current Capacity**: $50\text{ kA} - 300\text{ kA}$ per phase.
* **Voltage Protection Rating (VPR)**: Clamping voltage ratings per UL 1449.
* **Short-Circuit Rating (SCCR)**: $200\text{ kA}$ withstand rating.

---

## 3. Python Example
```python
from james_app.core.power_quality import SurgeProtectiveDeviceObject, SpdType

spd = SurgeProtectiveDeviceObject(
    id="spd_main",
    tag="SPD-1",
    name="Main Service Entrance Surge Suppressor",
    spd_type=SpdType.TYPE_1,
    surge_capacity_ka_per_phase=200.0,
    short_circuit_current_rating_sccr_ka=200.0
)
```
