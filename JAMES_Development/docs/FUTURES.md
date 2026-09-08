# JEMBY / JAMES: Future Innovations & AI Roadmap

This document outlines the strategic future capabilities, advanced AI integrations, and architectural enhancements planned for the **JEMBY JAMES Electrical Digital Twin Platform**.

---

## 1. Multimodal AI Nameplate OCR & Field Vision Engine

### 1.1 Overview
Surveyors spend substantial on-site time manually transcribing worn, stamped metal nameplates across hundreds of facility electrical assets. The AI Vision Engine will enable surveyors to snap a single photo of an equipment nameplate, with Gemini Multimodal models automatically parsing, extracting, and populating structured attributes in the Cockpit.

```mermaid
flowchart LR
    A["📸 Surveyor Snaps Nameplate Photo"] --> B["Multimodal Vision Agent (Gemini 2.5 Flash)"]
    B --> C["Structured JSON Extraction:
• Manufacturer: Square D
• Model No: NQ442L225
• Voltage: 208Y/120V 3Ø 4W
• Bus Amps: 225A
• AIC: 22 kA
• Serial No: 894021"]
    C --> D["Auto-Fills Nameplate Form & Dynamic Specs"]
    D --> E["Surveyor Reviews & Confirms with 1 Tap"]
```

### 1.2 Key Features:
* **Glare & Wear Invariance**: Processes stamped metal plates, embossed lettering, weathered outdoor tags, and dot-peen markings under uneven lighting.
* **Fuzzy Master Catalog Resolution**: Reconciles partially worn model numbers (e.g., `NQ44...`) against the Master Catalog to complete missing engineering ratings.
* **Contextual Dynamic Attribute Mapping**: Automatically extracts specialized archetype parameters (e.g., `%Z = 5.75%` for transformers, `Prime kW = 750` for generators, or `Class R Fuses = 100A` for disconnects) directly into `vendor_attrs`.
* **Human-in-the-Loop Validation**: Highlights extracted values in the Cockpit UI with visual confidence indicators for instant surveyor verification.

---

## 2. Panel Directory OCR & Automated Schedule Digitization

### 2.1 Overview
Physical paper panel directories taped inside panelboard doors often contain handwritten or typewritten circuit descriptions, breaker sizes, and load destinations. 

```mermaid
flowchart TD
    A["📷 Photo of Panel Directory Card"] --> B["Table Structure & OCR Extraction Agent"]
    B --> C["Parsed Schedule Matrix:
Slot 1-3: 50A 2P 'Server Rack 1A'
Slot 2: 20A 1P 'HVAC Fan 1'
Slot 4: Space / Spare"]
    C --> D["Auto-Populates Dual-Column Schedule in Cockpit"]
    D --> E["Instant Single-Line Diagram Topology Edge Wiring"]
```

### 2.2 Key Features:
* **Handwritten & Typewritten Text Recognition**: Reads handwritten circuit descriptions and pencil marks.
* **Slot Alignment & Multi-Pole Detection**: Distinguishes 1-pole, 2-pole, and 3-pole tied breakers and assigns them to odd/even left/right slot positions.
* **Automatic Downstream Load Mapping**: Parses circuit names (e.g., `AHU-3`, `Lighting ER-101`, `Chiller Pump 2`) and automatically matches them to existing equipment in the stack.

---

## 3. Master Catalog Governance & Field Back-Propagation

### 3.1 Overview
When field surveyors discover and record novel equipment attributes using the **`➕ Add Field Attribute`** tool, these tags initially attach strictly to that individual asset instance. This preserves catalog hygiene while offering infinite field flexibility.

```mermaid
flowchart LR
    A["Field Surveyor Adds Custom Tag:
'Enclosure Sound: 68 dBA'"] --> B["Stored in Local Instance vendor_attrs"]
    B --> C["Telemetry / Usage Aggregation"]
    C --> D{"Frequent Tag Across Multiple Sites?"}
    D -- Yes --> E["Governance Curation Queue"]
    E --> F["Promote to Master Catalog Schema"]
    D -- No --> G["Retain as Instance Tag"]
```

### 3.2 Key Features:
* **Per-Instance Isolation**: Ensures field creativity does not pollute global schemas or cause breaking database alterations.
* **Telemetry & Tag Frequency Heatmaps**: Identifies recurring custom parameters across client portfolios.
* **One-Click Promotion Workflow**: Catalog administrators can formally promote validated attributes into the global Master Catalog.

---

## 4. Time-Current Characteristic (TCC) & Selective Coordination

### 4.1 Overview
Integration between the Master Catalog breaker models and standardized Time-Current Curves (TCC) to automate electrical protection engineering.

```mermaid
flowchart LR
    A["Catalog Model (e.g. MasterPact MTZ)"] --> B["Parametric TCC Mathematical Curve Engine"]
    B --> C["Upstream vs Downstream Curve Superposition"]
    C --> D["Automated Miscoordination & Arc Flash Hazard Alert"]
```

### 4.2 Key Features:
* **Manufacturer Trip Curve Library**: Stores Long-Time (L), Short-Time (S), Instantaneous (I), and Ground-Fault (G) settings for Square D, Eaton, Siemens, and ABB trip units.
* **Automated Overlap Detection**: Warns engineers if a downstream branch breaker will trip upstream main protection.
* **Arc Flash Boundary Estimation**: Uses IEEE 1584 calculations based on breaker clearing times and short-circuit current.

---

## 5. Infrared (IR) Thermography & Field Sensor Integration

### 5.1 Overview
Direct attachment of thermal imaging camera data (FLIR, Seek Thermal) to circuit breaker slots, transformer coils, and cable lugs.

### 5.2 Key Features:
* **Radiometric Photo Embedding**: Stores thermal images with temperature metadata per slot.
* **Delta-T Thermal Anomaly Flagging**: Automatically calculates $\Delta T$ against adjacent phases and highlights overheating lugs in the SLD and Panel Schedule.
* **Preventive Maintenance Ticketing**: Generates immediate work orders for loose connections or phase load imbalances.

---

## 6. Offline-First Progressive Web App (PWA) Field Mode

### 6.1 Overview
Full offline operation for industrial basements, electrical vaults, mines, and remote substations with zero internet connectivity.

### 6.2 Key Features:
* **Local SQLite / WASM Storage**: Full client-side database running in the browser engine via WebAssembly.
* **Background Delta Sync**: Automatically reconciles and merges offline field surveys back into the central cloud repository when connectivity is restored.
* **Compressed Image Queuing**: Efficiently manages high-resolution nameplate and inspection photos offline before uploading.

---

## 7. Global Shared Master Catalog & Multi-Project Workspace Provisioning

### 7.1 Overview
The Master Catalog (`data/master_catalog.db`) functions as a single global source of truth across all survey projects. Each client facility maintains its own isolated digital twin SQLite database (`data/clients/{client_id}/{facility_id}/model.db`).

### 7.2 Key Features:
* **Shared Component Library**: All archetypes, voltage tiers, and manufacturer SKUs created in the Catalog Studio are instantly accessible to any survey project.
* **`[ + New Project... ]` Provisioning Wizard (under Files Menu)**: A dedicated workflow to spawn new client/facility projects, auto-create folder structures (`data/clients/{client_id}/{facility_id}/`), initialize clean SQLite `model.db` databases, and link to the global master catalog.
* **Dynamic Workspace Switching**: Allows surveyors to toggle between client facilities (e.g. *Zoetis B4*, *Pfizer CUP*, *Genentech B10*) on the fly without restarting the server.

