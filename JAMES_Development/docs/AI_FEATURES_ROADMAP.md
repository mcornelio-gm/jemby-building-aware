# JAMES Electrical Digital Twin: AI Features & Capabilities Roadmap

---

## 1. Executive Summary

The **JAMES Electrical Digital Twin** platform bridges physical field survey workflows with authoritative electrical engineering data models. By integrating multimodal AI and domain-grounded intelligence, JAMES transforms from a manual survey tool into an **autonomous electrical engineering copilot**—dramatically reducing field data collection time, eliminating data transcription errors, verifying National Electrical Code (NEC) compliance, and enabling predictive facility operational analysis.

---

## 2. Strategic AI Feature Matrix

```
                      HIGH VALUE
                          │
     [Nameplate OCR &     │    [Legacy SLD Blueprint
      Catalog Matching]   │     PDF Vectorizer]
                          │
     [Panel Directory     │    [Blast Radius Impact
      Matrix Parser]      │     Simulation Engine]
                          │
──────────────────────────┼───────────────────────────
                          │
     [NEC Rule & Voltage  │    [Infrared Thermal Hotspot
      Sanity Validator]   │     Diagnostic Assistant]
                          │
                          │
                      LOW VALUE
       LOW EFFORT ────────┼──────── HIGH EFFORT
```

---

## 3. Core Feature Pillars

### Pillar I: Multimodal Vision & Field Data Acceleration (Field Survey Superpowers)

1. **Nameplate OCR & Catalog Matching (Gemini Multimodal)**
   * **Problem**: Field electricians spend considerable time typing model numbers, AIC ratings, serial numbers, and full-load amps from dirty or inaccessible nameplates.
   * **Solution**: Electrician snaps a photo of an equipment nameplate (Eaton, Square D, Siemens, GE, Baldor, etc.).
   * **AI Execution**:
     * Extracts Volts, Phase, Poles, FLA, NEMA type, Frame size, AIC rating, and Serial Number.
     * Matches raw string extractions to normalized SKUs in the `Master Vendor Catalog`.
     * Auto-populates the survey form and locks in verified engineering tolerances.

2. **Panel Directory Photo-to-Schedule Transcriber**
   * **Problem**: Entering 42 or 84 circuit breaker rows with handwritten or faded directory labels takes 15–20 minutes per panel.
   * **Solution**: Take a high-resolution photo of the paper directory glued inside the panel door.
   * **AI Execution**:
     * Segregates Odd (Left) vs. Even (Right) slot columns.
     * Detects bracketed multi-pole ties (2P, 3P circuits).
     * Transcribes text (e.g. `AHU-1 Supply Fan`, `Lab Receptacles RM 104`, `Spare`).
     * Instantly populates the interactive breaker matrix.

3. **Legacy Single-Line Diagram (SLD) & Blueprint Ingestion**
   * **Problem**: Facilities have 30 years of scanned PDF blueprints and CAD drawings with no digital twin database.
   * **Solution**: Upload PDF single-line drawings into JAMES.
   * **AI Execution**:
     * Recognizes standard electrical symbols (Transformers, Main Switchboards, ATS, Breakers, Panelboards, Generators, VFDs).
     * Parses upstream/downstream connection lines and conductor sizes.
     * Generates a fully linked `model.db` / `model.jsonl` graph structure ready for verification.

4. **Infrared (IR) Thermal Inspection Diagnostic Assistant**
   * **Problem**: Thermographers take FLIR images during PM routines, but report generation and severity classification is manual.
   * **Solution**: Upload radiometric IR photos directly to an asset’s survey record.
   * **AI Execution**:
     * Detects hot-spot temperature deltas ($\Delta T$) between Phase A, B, and C bus stabs.
     * Automatically flags loose lugs, overloaded phases, or deteriorating breaker contacts according to NETA/NFPA 70B standards.

---

### Pillar II: Engineering Intelligence & Automated Topology Validation

1. **Topology Sanity & Voltage Mismatch Sentinel**
   * Real-time automated verification engine that audits the graph on every connection update:
     * **Voltage Incompatibility**: Flags if a 208Y/120V panel is fed from a 480V switchboard without an intermediate step-down transformer (`XFMR`).
     * **Ampacity & OCPD Violation**: Warns if an upstream 400A breaker feeds a panel with a 225A bus rating without proper secondary protection.
     * **Phase Rotation Discontinuity**: Ensures 3-phase source chains do not improperly feed single-phase designated downstream loads without tagging.

2. **Automated Arc Flash & NFPA 70E Pre-Computation**
   * Estimates available short-circuit current ($I_{sc}$) based on utility transformer size and impedance ($Z\%$).
   * Computes incident energy ($cal/cm^2$) at each panel bus.
   * Recommends required PPE category (Category 1–4) and prints standard compliant Arc Flash labels directly from JAMES.

3. **Conductor Sizing & Conduit Fill Calculation**
   * Given load FLA, distance, and conduit type, automatically calculates minimum copper conductor size, voltage drop ($< 3\%$ feeder, $< 5\%$ total), and conduit fill percentage (NEC Chapter 9).

---

### Pillar III: Conversational Digital Twin ("Chat with Your Facility")

1. **De-energization & "Blast Radius" Simulation**
   * Natural language query interface for facility managers and maintenance staff:
     * *Query*: `"What happens if I de-energize Feeder Space #7 on MDP-1 for 2 hours?"`
     * *AI Response*: Traverses the graph downstream and outputs:
       * Affected Panels: `LP-1A`
       * Critical Loads Dropped: `Central Plant Chiller CH-1`, `Chilled Water Pump P-1`
       * Affected Facility Areas: `Level 1 Cleanrooms`, `Penthouse Mechanical Room`
       * Standby Power Availability: Checks if ATS-1 can transfer critical loads to `GEN-1`.

2. **Predictive Capacity & Space Utilization Auditing**
   * *Query*: `"Where can I add a new 60A 480V 3-phase autoclaving machine on Floor 2?"`
   * *AI Response*: Scans all panels in Electric Room 201, evaluates unused physical slots/spaces, calculates remaining transformer kVA head-room, and suggests:
     * *`MCC-1 Buckets 13, 15, 17 (Available spare capacity: 120A, 480V 3P)`*.

3. **Compliance & Obsolescence Search**
   * *Query*: `"List all circuit breakers in the facility with AIC ratings below 25kA that are older than 15 years."`
   * *AI Response*: Returns a structured table of candidate assets for capital replacement planning.

---

### Pillar IV: Master Vendor Catalog AI Enrichment

1. **Autonomous Spec Sheet Extraction**
   * Crawls manufacturer technical datasheets (PDF cut-sheets from Eaton, Square D, Siemens, ABB, Generac) to auto-extract dimensions, trip curve parameters, interrupt ratings, and CAD port coordinates.

2. **Cross-Vendor Equivalent & Replacement Matcher**
   * Suggests drop-in catalog replacements when legacy equipment is marked as obsolete:
     * *Example*: Recommends contemporary *Eaton Power Defense Frame 2* equivalent for an obsolete *Westinghouse / Cutler-Hammer Series C* molded-case breaker.

---

## 4. Implementation Phasing

| Phase | Milestone / Features | Target Timeline |
| :--- | :--- | :--- |
| **Phase 1: Quick Wins** | • Nameplate Photo OCR & Catalog Matching<br>• Panel Directory Door Card Transcriber | Month 1–2 |
| **Phase 2: Graph Safety** | • Live Topology & Voltage Sanity Validator<br>• Automated Conductor & Conduit Sizing | Month 3–4 |
| **Phase 3: Digital Twin Chat** | • Natural Language Graph Traversal (Blast Radius Queries)<br>• Capacity & Spare Slot Search Assistant | Month 5–6 |
| **Phase 4: Advanced Vision** | • Legacy PDF Single-Line Blueprint Vectorizer<br>• FLIR Infrared Thermal Anomaly Classifier | Month 7+ |

---

## 5. Technical Architecture for AI Services

```
┌─────────────────────────────────────────────────────────────┐
│                 JAMES Frontend (Web / Mobile)               │
│         [Camera Capture]   [Interactive Graph]   [Chat UI]  │
└───────────────┬──────────────────────┬───────────────┬──────┘
                │                      │               │
                ▼                      ▼               ▼
   ┌──────────────────────┐ ┌────────────────────┐ ┌──────────────┐
   │ Multimodal Vision    │ │ Graph Analysis     │ │ LLM Facility │
   │ (Gemini 1.5 Pro /    │ │ (NetworkX /        │ │ Query Engine │
   │  Flash OCR Pipeline) │ │  SQLite Graph RAG) │ │ (LangChain/  │
   └──────────┬───────────┘ └─────────┬──────────┘ │  Tool Use)  │
              │                       │            └──────┬───────┘
              ▼                       ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                JAMES Core Data Layer (`db.py`)              │
│       `model.db` (SQLite)  •  `model.jsonl`  •  Catalog     │
└─────────────────────────────────────────────────────────────┘
```

---

*Document Author: JAMES Development & AI Systems Team*  
*Document Version: 1.0*  
*Reference File: `docs/AI_FEATURES_ROADMAP.md`*
