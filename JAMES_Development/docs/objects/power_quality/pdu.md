# Object Specification: Data Center Power Distribution Unit (PDU)

## 1. Overview
The **Data Center Power Distribution Unit (PDU)** (`PowerDistributionUnitObject`) is a specialized raised-floor high-density transformation and power distribution cabinet. It incorporates a clean-power K-13 isolation transformer ($480\text{V} \to 208\text{Y}/120\text{V}$), TVSS surge suppression, subfeed breakers, and two to four 42-pole output panelboards with continuous Branch Circuit Monitoring (BCM) for server racks.

* **Class**: `PowerDistributionUnitObject`
* **Parent**: `BaseElectricalObject`
* **Category**: `Data Center Power`

---

## 2. Technical Specifications
* **Isolation Transformer Capacity**: $75, 100, 150, 225, 300\text{ kVA}$.
* **Harmonic Rating**: $K\text{-13}$ or $K\text{-20}$ for data center switch-mode power supplies.
* **Output Circuit Density**: 42, 84, 126, or 168 pole branch breaker positions.
* **Branch Circuit Monitoring (BCM)**: Real-time current, active power (kW), and energy (kWh) logging per branch circuit.

---

## 3. Python Example
```python
from james_app.core.power_quality import PowerDistributionUnitObject

pdu = PowerDistributionUnitObject(
    id="pdu_pod_a",
    tag="PDU-1A",
    name="Server Pod A Dual PDU",
    kva_rating=150.0,
    primary_voltage=480.0,
    secondary_voltage=208.0,
    k_factor=13,
    total_branch_poles=84,
    has_branch_circuit_monitoring=True
)
```
