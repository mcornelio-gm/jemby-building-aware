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


class SiteConfig(BaseModel):
    """Configuration model for site profile and electrical service characteristics."""
    facility_name: str = Field(default="")
    street_address: Optional[str] = Field(default="")
    city: Optional[str] = Field(default="")
    state: Optional[str] = Field(default="")
    postal_code: Optional[str] = Field(default="")
    country: Optional[str] = Field(default="USA")

    # Electrical Service
    service_voltage: str = Field(default="480Y/277V 3Ø 4W")
    service_amperage: float = Field(default=3000.0)
    service_phase: int = Field(default=3)
    service_wires: int = Field(default=4)
    service_frequency: str = Field(default="60 Hz")
    service_type: str = Field(default="Underground Pad-Mounted")
    main_disconnect_type: str = Field(default="Main Circuit Breaker (MCB)")
    available_fault_current_ka: float = Field(default=65.0)

    # Utility Provider
    utility_name: Optional[str] = Field(default="")
    utility_account_number: Optional[str] = Field(default="")
    utility_meter_number: Optional[str] = Field(default="")
    utility_transformer_id: Optional[str] = Field(default="")

    # Key Contacts
    primary_contact_name: Optional[str] = Field(default="")
    primary_contact_title: Optional[str] = Field(default="")
    primary_contact_email: Optional[str] = Field(default="")
    primary_contact_phone: Optional[str] = Field(default="")
    emergency_contact_name: Optional[str] = Field(default="")
    emergency_contact_phone: Optional[str] = Field(default="")
    facility_operating_hours: str = Field(default="24/7 Operations")

    # Compliance & Safety
    nec_edition: str = Field(default="NEC 2023")
    arc_flash_study_date: Optional[str] = Field(default="")
    arc_flash_status: str = Field(default="Verified / Compliant")
    notes: Optional[str] = Field(default="")
    attributes: Dict[str, Any] = Field(default_factory=dict)

