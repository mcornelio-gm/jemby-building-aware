# Object Specification: Critical Power & Isolated Ground Panel (CP / EDP)

## 1. Overview
The **Critical Power Panelboard** is designed for sensitive IT gear, data centers, computer rooms, audio/broadcast studios, and laboratory instrumentation requiring clean power free of harmonic distortion and transient spikes.

* **Class**: `CriticalPowerPanelObject`
* **Parent**: `PanelboardObject`
* **Category**: `Critical IT & Isolated Ground`

---

## 2. Electrical Specifications
* **Nominal Voltage**: `120/208V 3Ø 4W`
* **Bus Continuous Ampacity**: `100A`, `225A`, `400A`
* **Isolated Ground (IG) Bus**: Dedicated isolated ground busbar electrically insulated from the metal panel enclosure to prevent ground loop noise (NEC 250.146(D)).
* **Surge Protection Device (SPD)**: Integrated SPD / TVSS module with per-phase surge ratings ($50\text{kA} - 200\text{kA}$).

---

## 3. Deterministic Rules & Validation
1. **Surge Protection Verification**: Warns if the integrated SPD rating is below the recommended $50\text{kA}$ minimum for mission-critical IT installations.
2. **Harmonic Sizing**: Encourages $200\%$ oversized neutral busbars to handle non-linear computer power supply triplen harmonics ($3^{\text{rd}}, 9^{\text{th}}, 15^{\text{th}}$).
3. **Circuit Tagging**: Circuits automatically prefix with `[IG/CLEAN]`.

---

## 4. Python Example
```python
from james_app.core.panels import CriticalPowerPanelObject

cp = CriticalPowerPanelObject.create_empty(
    panel_id="CP_SERVER_A",
    tag="CP-A",
    name="Server Room Critical Power",
    total_spaces=42,
    mains_rating_amps=225
)
cp.spd_rating_ka = 160.0

# Add clean server PDU circuit
cp.add_it_circuit(slot_start=1, description="Rack 1-4 Dual A Feeder", amps=30, poles=2)
```
