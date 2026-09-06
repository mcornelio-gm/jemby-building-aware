# Object Specification: Drawout Power Air Circuit Breaker (LVPCB)

## 1. Overview
The **Drawout Low Voltage Power Circuit Breaker (LVPCB / Air Circuit Breaker)** (`DrawoutPowerBreakerObject`) is a heavy-duty, high-withstand protective device engineered for low-voltage switchgear ($800\text{A} - 6000\text{A}$) and main electrical substation service entrances. It features a mechanical drawout racking carriage for live maintenance, high short-time withstand current ratings without instantaneous trip requirements, and microprocessor-based **LSIG** trip units.

* **Class**: `DrawoutPowerBreakerObject`
* **Parent**: `CircuitBreakerObject`
* **Category**: `Protective Device`

---

## 2. Technical Specifications
* **Frame Ratings**: $800\text{A}, 1600\text{A}, 2000\text{A}, 3200\text{A}, 4000\text{A}, 5000\text{A}, 6000\text{A}$
* **Short-Circuit Withstand Rating ($\text{AIC}$)**: $65\text{kA}, 85\text{kA}, 100\text{kA}, 150\text{kA}$ (30-cycle short-time withstand per ANSI C37.13 / UL 1066).
* **LSIG Electronic Trip Features**:
  * **L**: Long-Time Delay (Overload pickup & time band)
  * **S**: Short-Time Delay (Selective coordination pickup & delay)
  * **I**: Instantaneous Trip (High fault suppression)
  * **G**: Ground-Fault Pickup & Delay (Equipment protection)
* **Mechanism**: 3-position drawout racking (Connected, Test, Disconnected).
* **Compatible Enclosures**: Metal-Enclosed Low Voltage Switchgear, Main Substation Distribution.

---

## 3. Deterministic Rules & Validation
1. **Bulk Capacity Check**: Flags a warning if sized below $400\text{A}$, suggesting standard molded-case circuit breakers (`MoldedCaseBreakerObject`) for smaller branch feeds.
2. **Selective Coordination**: Verifies that LSIG trip curves coordinate with downstream distribution breakers.

---

## 4. Python Example
```python
from james_app.core.breakers import DrawoutPowerBreakerObject, BreakerStatus

lvpcb = DrawoutPowerBreakerObject(
    id="bkr_swg_main",
    tag="MAIN-SWG-1",
    name="Main Service Entrance Drawout Air Breaker",
    slot_start=1,
    poles=3,
    occupied_slots=[1, 2, 3],
    amps=3200,
    frame_amps=4000,
    aic_rating_ka=100.0,
    has_lsig_protection=True,
    is_drawout=True,
    status=BreakerStatus.ON,
    connected_phases=["A", "B", "C"]
)
```
