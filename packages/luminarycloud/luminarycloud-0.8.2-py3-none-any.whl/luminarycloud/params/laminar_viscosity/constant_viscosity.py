# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from luminarycloud.params.laminar_viscosity import LaminarViscosityModel


@dataclass(kw_only=True)
class ConstantViscosity(LaminarViscosityModel):
    """
    Constant laminar viscosity model.
    """

    constant: float = 1.7894e-05
    "Viscosity constant."
