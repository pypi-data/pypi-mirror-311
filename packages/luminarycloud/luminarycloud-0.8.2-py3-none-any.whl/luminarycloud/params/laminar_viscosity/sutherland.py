# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
from luminarycloud.params.laminar_viscosity import LaminarViscosityModel


@dataclass(kw_only=True)
class Sutherland(LaminarViscosityModel):
    """
    Sutherland viscosity model.
    """

    viscosity_ref: float = 1.716e-05
    "Dynamic viscosity at the reference temperature."
    viscosity_temp_ref: float = 273.15
    "Reference temperature."
    sutherland_constant: float = 110.4
    "Sutherland Constant."
