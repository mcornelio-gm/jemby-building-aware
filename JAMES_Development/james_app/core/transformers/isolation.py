"""Clean Power / Medical Isolation Transformer Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.transformers.base_transformer import (
    CoolingType,
    TransformerObject,
    WindingConfiguration,
)


class IsolationTransformerObject(TransformerObject):
    """
    Precision Isolation Transformer (1:1 Ratio or Step-Down).
    Engineered for data centers, sensitive IT equipment, and hospital operating rooms (NEC 517).
    Establishes a newly derived separately derived system (SDS) with zero common-mode electrical noise,
    dual electrostatic copper shielding, and dedicated isolated grounding reference.
    """
    category: str = "Clean Power Equipment"
    transformer_type_name: str = "Precision Isolation Transformer"
    primary_voltage: float = Field(default=480.0, description="Primary line-to-line voltage")
    secondary_voltage: float = Field(default=208.0, description="Secondary line-to-line voltage")
    secondary_neutral_voltage: Optional[float] = Field(default=120.0, description="Secondary line-to-neutral voltage")
    kva_rating: float = Field(default=50.0, description="Apparent power rating in kVA")
    has_dual_electrostatic_shield: bool = Field(default=True, description="Double copper Faraday shield between windings")
    common_mode_attenuation_db: int = Field(default=120, description="Common-mode noise attenuation in dB (e.g. 120dB)")
    transverse_mode_attenuation_db: int = Field(default=30, description="Transverse-mode noise attenuation in dB (e.g. 30dB)")
    k_factor: int = Field(default=13, description="Harmonic mitigation rating (K-13 / K-20)")
    is_medical_grade: bool = Field(default=False, description="Designed for healthcare wet procedure locations (NEC 517)")

    def validate_rules(self) -> List[str]:
        """Perform isolation transformer code compliance checks."""
        warnings = super().validate_rules()
        if self.k_factor < 4 and not self.is_medical_grade:
            warnings.append(
                f"Isolation Transformer {self.tag}: Clean power IT isolation units recommend K-Factor >= 4 (got K-{self.k_factor})."
            )
        return warnings
