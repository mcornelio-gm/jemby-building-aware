"""Base Abstract Class and Unified Protocol for all JEMBY Electrical Objects."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BaseElectricalObject(BaseModel, ABC):
    """Abstract Base Class for all JEMBY Digital Twin Electrical Objects."""

    # 1. Universal Identity & Metadata
    id: str = Field(..., description="Unique global instance identifier")
    tag: str = Field(..., description="Engineering schematic tag (e.g. 'MDP-1', 'CB-17')")
    name: str = Field(..., description="Human-readable title/description")
    category: str = Field(default="General", description="Equipment classification")

    # 2. Connectivity Terminals (Ports)
    @abstractmethod
    def get_input_ports(self) -> List[str]:
        """Return list of upstream connection terminal port IDs."""
        pass

    @abstractmethod
    def get_output_ports(self) -> List[str]:
        """Return list of downstream load/branch connection terminal port IDs."""
        pass

    # 3. Deterministic Physics & Code Rules
    @abstractmethod
    def validate_rules(self) -> List[str]:
        """
        Evaluate deterministic physical rules (NEC sizing, phase continuity, bus limits).
        Returns a list of warning or error strings (empty if valid).
        """
        pass

    # 4. Multi-View Visual Projections
    @abstractmethod
    def compile_focused_dot(self) -> str:
        """Render the 1st-degree focused Graphviz DOT depiction."""
        pass

    @abstractmethod
    def render_html_view(self) -> str:
        """Render native HTML/Tailwind interactive component view."""
        pass

    @abstractmethod
    def compile_plantuml_sld(self) -> str:
        """Render quick-reference PlantUML Single-Line Diagram (SLD) representation."""
        pass

    # 5. Gemini AI Semantic Context
    def to_gemini_context(self) -> Dict[str, Any]:
        """Export standardized structured representation for Gemini AI analysis."""
        return self.model_dump()
