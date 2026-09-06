"""General Purpose Ventilated Dry-Type Step-Down Transformer Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.transformers.base_transformer import (
    CoolingType,
    TransformerObject,
    WindingConfiguration,
)


class DryTypeStepDownTransformerObject(TransformerObject):
    """
    Commercial / Industrial General Purpose Dry-Type Step-Down Transformer.
    Typically transforms 480V 3Ø primary power to 208Y/120V 3Ø 4W (or 480V to 120/240V 1Ø)
    for commercial lighting, receptacles, and office tenant distribution.
    Features ventilated NEMA 1/3R enclosure, DOE 2016 efficiency, and 220°C insulation.
    """
    category: str = "Distribution Transformer"
    transformer_type_name: str = "Dry-Type Step-Down Transformer"
    enclosure_nema_rating: str = Field(default="NEMA 1 (Indoor Ventilated)", description="NEMA enclosure type")
    sound_level_db: int = Field(default=50, description="Audible sound level rating in dBA (NEMA ST-20)")
    has_electrostatic_shield: bool = Field(default=False, description="Copper foil electrostatic shield between windings")
    winding_material: str = Field(default="Aluminum", description="Winding conductor material ('Aluminum' or 'Copper')")
    temperature_rise_c: int = Field(default=150, description="Temperature rise rating in °C (150°C, 115°C, or 80°C)")
    cooling_type: CoolingType = Field(default=CoolingType.ANN_AIR)
    winding_config: WindingConfiguration = Field(default=WindingConfiguration.DELTA_WYE)

    def validate_rules(self) -> List[str]:
        """Verify commercial dry-type specific parameters."""
        warnings = super().validate_rules()
        if self.temperature_rise_c not in [80, 115, 150]:
            warnings.append(
                f"Dry-Type Transformer {self.tag}: Temperature rise ({self.temperature_rise_c}°C) is non-standard (typical ratings are 80°C, 115°C, or 150°C)."
            )
        return warnings
