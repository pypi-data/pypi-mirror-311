# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass, field

import luminarycloud.params.enum as enum
import luminarycloud.params.laminar_viscosity as lv
from luminarycloud._helpers.defaults import _reset_defaults
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.materials import Material


@dataclass(kw_only=True)
class MaterialFluid(Material):
    """Configuration for Fluid materials"""

    reference_pressure: float = 0.0
    "Reference pressure for the simulation. Unless otherwise stated, all input pressure values will be relative to this field."
    laminar_viscosity_model: lv.LaminarViscosityModel = field(default_factory=lv.Sutherland)
    "Models available for the dynamic viscosity of the fluid."

    @abstractmethod
    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = super()._to_proto()
        _reset_defaults(_proto.material_fluid)
        _proto.material_fluid.reference_pressure.value = self.reference_pressure
        if isinstance(self.laminar_viscosity_model, lv.Sutherland):
            _proto.material_fluid.laminar_viscosity_model_newtonian = (
                enum.LaminarViscosityModelNewtonian.SUTHERLAND
            )
            _proto.material_fluid.sutherland_viscosity_ref.value = (
                self.laminar_viscosity_model.viscosity_ref
            )
            _proto.material_fluid.sutherland_viscosity_temp_ref.value = (
                self.laminar_viscosity_model.viscosity_temp_ref
            )
            _proto.material_fluid.sutherland_constant.value = (
                self.laminar_viscosity_model.sutherland_constant
            )
        elif isinstance(self.laminar_viscosity_model, lv.ConstantViscosity):
            _proto.material_fluid.laminar_viscosity_model_newtonian = (
                enum.LaminarViscosityModelNewtonian.LAMINAR_CONSTANT_VISCOSITY
            )
            _proto.material_fluid.laminar_constant_viscosity_constant.value = (
                self.laminar_viscosity_model.constant
            )
        elif isinstance(self.laminar_viscosity_model, lv.TemperatureDependentViscosity):
            _proto.material_fluid.laminar_viscosity_model_newtonian = (
                enum.LaminarViscosityModelNewtonian.TEMPERATURE_DEPENDENT_LAMINAR_VISCOSITY
            )
            _proto.material_fluid.dynamic_viscosity_table_data = (
                self.laminar_viscosity_model.dynamic_viscosity_table_data
            )
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.MaterialEntity):
        super()._from_proto(proto)
        self.reference_pressure = proto.material_fluid.reference_pressure.value
        if (
            proto.material_fluid.laminar_viscosity_model_newtonian
            == enum.LaminarViscosityModelNewtonian.SUTHERLAND
        ):
            self.laminar_viscosity_model = lv.Sutherland(
                viscosity_ref=proto.material_fluid.sutherland_viscosity_ref.value,
                viscosity_temp_ref=proto.material_fluid.sutherland_viscosity_temp_ref.value,
                sutherland_constant=proto.material_fluid.sutherland_constant.value,
            )
        elif (
            proto.material_fluid.laminar_viscosity_model_newtonian
            == enum.LaminarViscosityModelNewtonian.LAMINAR_CONSTANT_VISCOSITY
        ):
            self.laminar_viscosity_model = lv.ConstantViscosity(
                constant=proto.material_fluid.laminar_constant_viscosity_constant.value
            )
        elif (
            proto.material_fluid.laminar_viscosity_model_newtonian
            == enum.LaminarViscosityModelNewtonian.TEMPERATURE_DEPENDENT_LAMINAR_VISCOSITY
        ):
            self.laminar_viscosity_model = lv.TemperatureDependentViscosity(
                dynamic_viscosity_table_data=proto.material_fluid.dynamic_viscosity_table_data
            )
