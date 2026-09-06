"""Liquid-Filled Padmounted Substation Transformer Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.transformers.base_transformer import (
    CoolingType,
    TransformerObject,
    WindingConfiguration,
)


class LiquidFilledPadmountTransformerObject(TransformerObject):
    """
    Outdoor Liquid-Filled Padmounted Substation Transformer.
    Step-down transformer transforming medium-voltage utility distribution (e.g. 13.8kV, 12.47kV, 4.16kV)
    down to low-voltage building service entrances (480Y/277V or 208Y/120V) for commercial campuses,
    industrial facilities, and large institutional sites (500 kVA - 5000 kVA).
    """
    category: str = "Substation Transformer"
    transformer_type_name: str = "Liquid-Filled Padmount Transformer"
    primary_voltage: float = Field(default=12470.0, description="Medium-voltage primary rating in Volts")
    secondary_voltage: float = Field(default=480.0, description="Low-voltage secondary rating in Volts")
    secondary_neutral_voltage: Optional[float] = Field(default=277.0, description="Secondary phase-to-neutral rating")
    kva_rating: float = Field(default=1500.0, description="Apparent power capacity in kVA (e.g. 500, 750, 1000, 1500, 2000, 2500)")
    dielectric_fluid: str = Field(default="FR3 (Less-Flammable Seed Oil)", description="Dielectric insulating fluid ('FR3', 'Mineral Oil', 'Synthetic Ester')")
    cooling_type: CoolingType = Field(default=CoolingType.KNAN_LESS_FLAMMABLE)
    impedance_pct_z: float = Field(default=5.75, description="Percent impedance (%Z)")
    has_bayonet_fusing: bool = Field(default=True, description="Primary bay-o-net current-sensing fuse with isolation link")
    is_dead_front: bool = Field(default=True, description="Dead-front construction with 200A/600A loadbreak/deadbreak bushings")
    containment_required: bool = Field(default=True, description="Secondary oil spill containment required per IEEE/EPA guidelines")

    def validate_rules(self) -> List[str]:
        """Perform padmount safety and rating checks."""
        warnings = super().validate_rules()
        if self.kva_rating < 300.0:
            warnings.append(
                f"Padmount Transformer {self.tag}: Liquid-filled padmount units are typically >= 300 kVA (got {self.kva_rating} kVA)."
            )
        if self.primary_voltage < 1000.0:
            warnings.append(
                f"Padmount Transformer {self.tag}: Padmount transformers typically step down from medium-voltage (>1000V, got {self.primary_voltage}V)."
            )
        return warnings
