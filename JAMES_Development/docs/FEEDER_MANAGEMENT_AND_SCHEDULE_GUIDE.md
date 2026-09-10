# Feeder Management, Sizing & Schedule Guide
**JAMES Electrical Digital Twin — Technical Reference & Workflow Specification**

---

## 1. Industry Standard Feeder Concepts & Architecture

In commercial and industrial electrical distribution, **Feeders** are the critical power conductors that transmit bulk electrical energy from the primary service entrance or power sources (utility transformers, generators, UPS systems, switchgear) to downstream distribution equipment (subpanels, motor control centers, branch distribution switchboards).

Unlike **Branch Circuits** (which supply final utilization equipment or receptacles), feeders are governed by stringent National Electrical Code (NEC) standards:
- **NEC Article 215**: Feeder sizing, minimum ampacity ratings, and overcurrent protection requirements.
- **NEC Article 310**: Conductor materials (Copper vs. Aluminum), insulation types (THHN/THWN-2, XHHW-2), temperature ratings ($75^\circ\text{C}$ / $90^\circ\text{C}$ terminals), and ampacity tables (NEC Table 310.16).
- **NEC Chapter 9**: Conduit and tubing fill tables (40% maximum fill for 3 or more conductors).
- **NEC Article 250.122**: Minimum Equipment Grounding Conductor (EGC) sizing based on upstream overcurrent protection device (OCPD) rating.

---

## 2. Dedicated Feeder Pages & Feeder Schedule Table

The JAMES Digital Twin platform provides a dedicated **Feeder Schedule Table** accessible directly from the top navigation bar and Toolbox Bento Menu (`⚡ Feeders`).

### Key Features of the Feeder Schedule:
1. **Interactive Multi-Column Sorting**:
   - **Feeder Tag / ID**: Unique identifier (e.g., `FDR-MDP1-LP1`, `FDR-ATS-EMER`).
   - **Source (Fed From)**: Upstream origin device, bus, or breaker slot.
   - **Destination (Feeds To)**: Downstream load or distribution node.
   - **Length (ft)**: Total run length in feet.
   - **Conductor Size & Material**: Conductor gauge (`#12 AWG` through `750 kcmil`) and metal (`Copper` vs. `Aluminum`).
   - **Parallel Sets**: Number of conductors per phase (e.g., $2 \times 350\text{ kcmil}$, $4 \times 500\text{ kcmil}$).
   - **Raceway / Conduit**: Conduit type (`EMT`, `RMC`, `PVC`, `Cable Tray`) and trade diameter (`1/2"` to `4"`).
   - **Operating Voltage & Phase**: System voltage ($480\text{V } 3\phi$, $208\text{V } 3\phi$, $120/240\text{V } 1\phi$).
   - **Calculated Voltage Drop (%)**: Real-time calculated voltage drop percentage with color-coded compliance badges (Green $<3\%$, Amber $3-5\%$, Red $>5\%$).
2. **Search & Filter**: Real-time text filter by node name, floor location, conductor material, or deficiency status.
3. **Quick Edit Action**: Clicking any row immediately opens the feeder in the interactive Feeder Configuration Modal.

---

## 3. Interactive SLD Diagram & Survey Mode Workflows

Feeder conductors are visualized as interactive directed edges in the Single-Line Diagram (SLD).

### A. Diagram Mode Edge Interaction:
- **Clickable Edge Paths & Head/Tail Labels**: Users can click directly on the feeder line or its connection terminals on equipment boxes to inspect and configure the feeder.
- **Visual Selection Highlighting**: When selected, the active feeder edge glows in high-contrast cyan (`#00f0ff` / `#3b82f6`) with an active stroke width and drop-shadow.
- **Automatic Deselection on Close**: Closing the feeder configuration modal automatically removes the active selection halo and restores standard edge styling.
- **Layering & Z-Index Management**: The feeder modal slide-over drawer operates on a dedicated elevation layer, preventing collision or hiding underneath device attribute forms.

### B. Survey Mode Feeder Verification:
- **Field Data Collection**: Field electricians record measured feeder lengths, verify physical conductor markings, nameplate conduit tags, and record insulation condition during site walks.
- **Fed-From Validation**: Intelligent dropdown validation ensures terminal equipment (e.g., rooftop units, chillers) cannot be accidentally assigned as upstream feeder sources.

---

## 4. Engineering Calculations & Code Rules

The feeder calculation engine (`james_app/feeder_calculator.py`) evaluates conductors against deterministic electrical physics and NEC code requirements:

### A. Voltage Drop Formula
For 3-Phase balanced AC systems:
$$\Delta V = \frac{\sqrt{3} \times K \times I \times L}{CM}$$
$$\% \text{ Voltage Drop} = \left( \frac{\Delta V}{V_{\text{nominal}}} \right) \times 100$$

Where:
- $K = 12.9\ \Omega\cdot\text{cmil/ft}$ for Copper conductors (or $21.2$ for Aluminum).
- $I =$ Operating load current in Amperes.
- $L =$ One-way feeder length in feet.
- $CM =$ Conductor cross-sectional area in Circular Mils (multiplied by the number of parallel sets).

### B. Code Compliance Thresholds
- **NEC 210.19(A) / 215.2(A)(1) Advisory**: Feeder conductors sized so that voltage drop does not exceed **3.0%** at maximum connected load, and total combined feeder + branch circuit drop does not exceed **5.0%**.
- **Conduit Fill**: Total cross-sectional area of insulated conductors cannot exceed **40%** of total conduit interior area for 3+ conductors.
- **Equipment Grounding**: Sized according to NEC Table 250.122 based on the upstream breaker frame/trip rating.

---

## 5. Feeder API Endpoints

The JAMES backend exposes dedicated endpoints for feeder data and calculation:
- `GET /api/feeders` — Returns the complete list of project feeder edges with computed ampacity, length, and voltage drop metrics.
- `GET /api/feeders/{feeder_id}` — Retrieves detailed conductor specification, raceway details, and source/destination mappings.
- `POST /api/feeders/calculate` — Takes electrical parameters (`amps`, `length_ft`, `voltage`, `phase`, `metal`, `size_awg_kcmil`, `sets`) and returns precise voltage drop, ampacity rating, and NEC compliance flags.
