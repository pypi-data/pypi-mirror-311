from dataclasses import dataclass
from luminarycloud.params.laminar_thermal_conductivity import (
    LaminarThermalConductivityModel,
)


@dataclass(kw_only=True)
class ConstantLaminarPrandtl(LaminarThermalConductivityModel):
    """
    Constant laminar Prandtl number model.
    """

    prandtl: float = 0.72
    "Constant Prandtl number value."
