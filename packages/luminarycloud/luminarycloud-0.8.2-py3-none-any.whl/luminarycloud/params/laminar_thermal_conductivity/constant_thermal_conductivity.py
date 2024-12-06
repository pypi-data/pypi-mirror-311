from dataclasses import dataclass
from luminarycloud.params.laminar_thermal_conductivity import (
    LaminarThermalConductivityModel,
)


@dataclass(kw_only=True)
class ConstantThermalConductivity(LaminarThermalConductivityModel):
    """
    Constant thermal conductivity model.
    """

    conductivity: float = 0.0257
    "Constant thermal conductivity value."
