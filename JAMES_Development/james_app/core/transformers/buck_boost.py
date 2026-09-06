"""Buck-Boost Specialty Autotransformer Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.transformers.base_transformer import (
    CoolingType,
    TransformerObject,
    WindingConfiguration,
)


class BuckBoostTransformerObject(TransformerObject):
    """
    Buck-Boost Specialty Autotransformer.
    Compact 4-winding insulating transformer connected as an autotransformer to provide
    slight continuous voltage boost (+5% to +20%) or buck (-5% to -20%) for mismatched OEM equipment
    (e.g., operating a 230V European / Canadian motor on a standard 208V American supply, or 240V to 208V).
    """
    category: str = "Specialty Transformer"
    transformer_type_name: str = "Buck-Boost Autotransformer"
    kva_rating: float = Field(default=5.0, description="Nameplate isolated kVA rating")
    autotransformer_load_kva: float = Field(default=45.0, description="Connected apparent power capacity when wired as autotransformer")
    primary_voltage: float = Field(default=208.0, description="Line supply voltage in Volts")
    secondary_voltage: float = Field(default=230.0, description="Boosted or bucked load voltage in Volts")
    boost_buck_percentage: float = Field(default=10.58, description="Percentage voltage change (+ for boost, - for buck)")
    winding_config: WindingConfiguration = Field(default=WindingConfiguration.SINGLE_PHASE)
    primary_phases: int = Field(default=1, description="Single phase unit (often grouped in pairs for 3-phase)")
    secondary_phases: int = Field(default=1)

    def validate_rules(self) -> List[str]:
        """Perform buck-boost application safety checks."""
        warnings = []
        if abs(self.secondary_voltage - self.primary_voltage) > (0.30 * self.primary_voltage):
            warnings.append(
                f"Buck-Boost Transformer {self.tag}: Voltage delta ({abs(self.secondary_voltage - self.primary_voltage):.0f}V) exceeds typical autotransformer range (<=25%). For larger ratios, use a standard isolation step-down transformer."
            )
        return warnings
