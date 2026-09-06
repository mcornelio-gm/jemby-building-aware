# Object Specification: Base Electrical Object (Universal Protocol)

## 1. Overview
The **Base Electrical Object** (`BaseElectricalObject`) is the foundational abstract base class (ABC) for all Digital Twin entities across the JEMBY electrical modeling architecture. It enforces a strict **5-Facet Protocol** ensuring every physical or logical component (panels, breakers, cables, transformers, disconnects, placeholders) conforms to uniform identity, topology, physical validation, multi-view visual projection, and AI semantic interoperability.

* **Class**: `BaseElectricalObject`
* **Parent**: `pydantic.BaseModel`, `abc.ABC`
* **Module**: `james_app.core.base`

---

## 2. The 5-Facet Architectural Protocol

```
+---------------------------------------------------------------------------------+
|                              BaseElectricalObject                               |
+---------------------------------------------------------------------------------+
|  1. Universal Identity & Metadata   | id, tag, name, category                   |
|  2. Connectivity Terminals (Ports)  | get_input_ports(), get_output_ports()     |
|  3. Deterministic Physics & Rules   | validate_rules() -> List[str]             |
|  4. Multi-View Visual Projections   | DOT, HTML/Tailwind, PlantUML SLD          |
|  5. Gemini AI Semantic Context      | to_gemini_context() -> Dict[str, Any]     |
+---------------------------------------------------------------------------------+
```

### Facet 1: Universal Identity & Metadata
* `id: str`: Globally unique identifier across project workspaces (e.g. `"panel_mdp_1"`, `"cable_feed_101"`).
* `tag: str`: Formal engineering schematic tag (e.g. `"MDP-1"`, `"CB-17"`, `"T-1"`).
* `name: str`: Human-readable descriptive name (e.g. `"Main Power Distribution Panel"`).
* `category: str`: Standardized classification for matching and grouping (e.g. `"Main Power Distribution"`, `"Protective Device"`, `"Conductor Run"`).

### Facet 2: Connectivity Terminals (Ports)
Defines topological node attachment points for downstream graph traversal, power flow propagation, and voltage drop aggregation:
* `get_input_ports() -> List[str]`: Upstream line-side terminals (e.g. `["main"]`, `["bus_stab_1", "bus_stab_3"]`).
* `get_output_ports() -> List[str]`: Downstream load-side terminals (e.g. `["ckt_1_3_5"]`, `["load_terminal"]`).

### Facet 3: Deterministic Physics & Code Rules
* `validate_rules() -> List[str]`: Evaluates strict physical and NEC/NFPA electrical code constraints (ampacity limits, voltage drop $<3\%$, phase balancing $<15\%$, enclosure sizing $\ge 20\%$ spare capacity). Returns deterministic warning/error strings without relying on LLM hallucination.

### Facet 4: Multi-View Visual Projections
A single underlying Pydantic Digital Twin renders three distinct, synchronized projections:
1. `compile_focused_dot() -> str`: Focused 1st-degree Graphviz DOT syntax with HTML table styling and port handles.
2. `render_html_view() -> str`: Interactive, responsive native HTML component styled with Tailwind CSS tokens.
3. `compile_plantuml_sld() -> str`: High-level PlantUML Single-Line Diagram (SLD) representation.

### Facet 5: Gemini AI Semantic Context
* `to_gemini_context() -> Dict[str, Any]`: Generates sanitized, machine-readable JSON structured context for LLM prompt grounding and automated schematic generation.

---

## 3. Class Definition
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel, Field

class BaseElectricalObject(BaseModel, ABC):
    id: str = Field(..., description="Unique global instance identifier")
    tag: str = Field(..., description="Engineering schematic tag")
    name: str = Field(..., description="Human-readable title/description")
    category: str = Field(default="General", description="Equipment classification")

    @abstractmethod
    def get_input_ports(self) -> List[str]: ...

    @abstractmethod
    def get_output_ports(self) -> List[str]: ...

    @abstractmethod
    def validate_rules(self) -> List[str]: ...

    @abstractmethod
    def compile_focused_dot(self) -> str: ...

    @abstractmethod
    def render_html_view(self) -> str: ...

    @abstractmethod
    def compile_plantuml_sld(self) -> str: ...

    def to_gemini_context(self) -> Dict[str, Any]:
        return self.model_dump()
```
