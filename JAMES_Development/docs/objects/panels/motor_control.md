# Object Specification: Motor Control Center (MCC)

## 1. Overview
A **Motor Control Center (MCC)** is a floor-mounted, modular assembly of vertical steel sections containing plug-in combination motor control units ("buckets") for centralized starting, reversing, and speed control of electric motors.

* **Class**: `MotorControlCenterObject`
* **Parent**: `PanelboardObject`
* **Category**: `Motor Control Center`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `277/480V 3Ø 4W` or `480V 3Ø 3W`
* **Horizontal Main Busbar**: `600A`, `800A`, `1200A`, `2000A` (Tin-plated or Silver-plated Copper)
* **Vertical Busbar**: `300A` or `600A` per vertical section
* **Enclosure**: NEMA 1 (General Indoor), NEMA 12 (Industrial Dust-tight), NEMA 4X (Washdown)
* **Standard Sections**: Typically 2 to 10 vertical sections (each 20" wide $\times$ 90" high)

---

## 3. Modular "Buckets" & Protection Devices
* **Combination Motor Starters**: Magnetic contactor + solid-state overload relay + Motor Circuit Protector (MCP).
* **NEMA Sizes**: Size 1 ($27\text{A}$), Size 2 ($45\text{A}$), Size 3 ($90\text{A}$), Size 4 ($135\text{A}$), Size 5 ($270\text{A}$).
* **Variable Frequency Drives (VFDs)**: Integrated inverter buckets for precision motor speed control.
* **Matched Breaker Type**: `MotorCircuitProtectorObject` (MCP / Instantaneous-only mag trip).

---

## 4. Deterministic Rules (NEC 430)
1. **MCP Sizing (NEC 430.52)**: Instantaneous magnetic trip units sized up to $250\%$ of motor Full Load Amperes (FLA) to allow high starting inrush without nuisance tripping.
2. **3-Phase Motor Consistency**: Triggers a warning if single-phase breakers are inserted into an industrial MCC.

---

## 5. Python Example
```python
from james_app.core.panels import MotorControlCenterObject

mcc = MotorControlCenterObject.create_empty(
    panel_id="MCC_1",
    tag="MCC-1",
    name="Central Chiller Plant MCC",
    total_spaces=42,
    mains_rating_amps=800
)

# Add a 50HP Chilled Water Pump combination starter
mcc.add_motor_starter_bucket(
    slot_start=1,
    motor_name="Chilled Water Pump 1",
    hp_rating=50.0,
    fl_amps=65.0,
    nema_size=3,
    is_vfd=True
)
```
