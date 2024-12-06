# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.materials import MaterialFluid
from luminarycloud.params.laminar_thermal_conductivity import (
    LaminarThermalConductivityModel,
)
import luminarycloud.params.laminar_thermal_conductivity as ltc


# TODO: Add boussinesq_approximation parameters.
@dataclass(kw_only=True)
class ConstantDensityEnergy(MaterialFluid):
    """Configuration for Constant Density Energy materials"""

    constant_density_value: float = 1.225
    "Constant density value."
    specific_heat_cp: float = 1004.703
    "Specific heat at constant pressure."
    laminar_thermal_conductivity_model: LaminarThermalConductivityModel = field(
        default_factory=ltc.ConstantLaminarPrandtl
    )
    "Model for the laminar thermal conductivity of a fluid."

    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = super()._to_proto()
        _proto.material_fluid.density_relationship = (
            enum.DensityRelationship.CONSTANT_DENSITY_ENERGY
        )
        _proto.material_fluid.constant_density_value.value = self.constant_density_value
        _proto.material_fluid.specific_heat_cp.value = self.specific_heat_cp
        if isinstance(self.laminar_thermal_conductivity_model, ltc.ConstantLaminarPrandtl):
            _proto.material_fluid.laminar_thermal_conductivity = (
                enum.LaminarThermalConductivity.LAMINAR_CONSTANT_THERMAL_PRANDTL
            )
            _proto.material_fluid.laminar_constant_thermal_prandtl_constant.value = (
                self.laminar_thermal_conductivity_model.prandtl
            )
        elif isinstance(self.laminar_thermal_conductivity_model, ltc.ConstantThermalConductivity):
            _proto.material_fluid.laminar_thermal_conductivity = (
                enum.LaminarThermalConductivity.LAMINAR_CONSTANT_THERMAL_CONDUCTIVITY
            )
            _proto.material_fluid.laminar_constant_thermal_conductivity_constant.value = (
                self.laminar_thermal_conductivity_model.conductivity
            )
        else:
            raise ValueError("Unsupported laminar thermal conductivity model")
        return _proto

    def _from_proto(self, proto: clientpb.MaterialEntity):
        super()._from_proto(proto)
        self.constant_density_value = proto.material_fluid.constant_density_value.value
        self.specific_heat_cp = proto.material_fluid.specific_heat_cp.value
        if (
            proto.material_fluid.laminar_thermal_conductivity
            == enum.LaminarThermalConductivity.LAMINAR_CONSTANT_THERMAL_PRANDTL
        ):
            self.laminar_thermal_conductivity_model = ltc.ConstantLaminarPrandtl(
                prandtl=proto.material_fluid.laminar_constant_thermal_prandtl_constant.value
            )
        elif (
            proto.material_fluid.laminar_thermal_conductivity
            == enum.LaminarThermalConductivity.LAMINAR_CONSTANT_THERMAL_CONDUCTIVITY
        ):
            self.laminar_thermal_conductivity_model = ltc.ConstantThermalConductivity(
                conductivity=proto.material_fluid.laminar_constant_thermal_conductivity_constant.value
            )
