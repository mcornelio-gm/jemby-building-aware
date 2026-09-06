"""Pydantic Models for Project Topology, Equipment Nodes, and Feeder Edges."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Node(BaseModel):
    """Represents an equipment node instance in the electrical graph."""
    type: str = Field(..., description="Equipment type code from Master Catalog (e.g. SWBD, XFMR, ATS)")
    label: str = Field(..., description="Display label for the equipment instance (e.g. SWBD-MSB-2)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Attribute key-value data corresponding to catalog fields")


class Edge(BaseModel):
    """Represents an electrical connection / feeder between equipment ports."""
    id: str = Field(..., description="Unique edge identifier (e.g. edge_msb2_pnlm1)")
    from_node: str = Field(..., description="Source node ID")
    from_port: str = Field(default="out", description="Source port identifier on node (e.g. p1, out)")
    to_node: str = Field(..., description="Destination node ID")
    to_port: str = Field(default="in", description="Destination port identifier on node (e.g. in, norm)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Feeder attributes (e.g. breaker, fuse, cable)")


class Project(BaseModel):
    """Represents a complete electrical single-line diagram project topology."""
    project_id: str = Field(..., description="Unique project slug/ID")
    name: str = Field(..., description="Project human-readable title")
    nodes: Dict[str, Node] = Field(default_factory=dict, description="Map of node ID to Node instance")
    edges: List[Edge] = Field(default_factory=list, description="List of connected edges")


class FieldSchema(BaseModel):
    """Schema metadata for a dynamic equipment field."""
    type: str
    label: str
    required: bool = False
    default: Optional[Any] = None
    options: Optional[List[Any]] = None


class EquipmentSchema(BaseModel):
    """Schema metadata for an equipment category."""
    category: str
    name: str
    symbol_code: str
    fields: Dict[str, FieldSchema]
