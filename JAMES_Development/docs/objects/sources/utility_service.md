# Object Specification: Utility Service Entrance Source

## 1. Overview
The **Utility Service Entrance Source** (`UtilityServiceSource`) models the primary electrical grid connection from the utility provider (e.g., ConEd, PG&E, National Grid). It defines the point of common coupling (PCC), available utility short-circuit MVA ($S_{sc}$), impedance $X/R$ ratio for fault calculation studies, and revenue metering CT/PT compartments.

* **Class**: `UtilityServiceSource`
* **Parent**: `PowerSourceObject`
* **Category**: `Utility Service`

---

## 2. Technical Specifications
* **Utility Parameters**:
  * `utility_company_name`: Operating utility provider
  * `service_entrance_type`: Underground Lateral or Overhead Service Drop
  * `available_fault_mva_sc`: Primary available fault MVA ($100 - 1000\text{ MVA}$)
  * `xr_ratio`: System short-circuit $X/R$ ratio at service entrance ($10 - 25$)
  * `has_revenue_metering_ct_pt`: Utility instrument metering section

---

## 3. Python Example
```python
from james_app.core.sources import UtilityServiceSource

util = UtilityServiceSource(
    id="src_util_1",
    tag="UTIL-1",
    name="Building 480V Utility Service",
    voltage=480.0,
    phases=3,
    capacity_kw=2000.0,
    capacity_kva=2500.0,
    available_fault_mva_sc=500.0,
    available_fault_current_ka=45.0,
    xr_ratio=15.0
)
```
