# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass
import luminarycloud.params._param_wrappers as w
from luminarycloud.params.laminar_viscosity import LaminarViscosityModel


@dataclass(kw_only=True)
class TemperatureDependentViscosity(LaminarViscosityModel):
    """
    Temperature dependent laminar viscosity model.
    """

    dynamic_viscosity_table_data: w.RectilinearTable
    "Correlation between dynamic viscosity and temperature."
