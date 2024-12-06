# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

import luminarycloud.params.enum as enum
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.materials import MaterialFluid


@dataclass(kw_only=True)
class ConstantDensity(MaterialFluid):
    """Configuration for Constant Density materials"""

    constant_density_value: float = 1.225
    "Constant density value."

    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = super()._to_proto()
        _proto.material_fluid.density_relationship = enum.DensityRelationship.CONSTANT_DENSITY
        _proto.material_fluid.constant_density_value.value = self.constant_density_value
        return _proto

    def _from_proto(self, proto: clientpb.MaterialEntity):
        super()._from_proto(proto)
        self.constant_density_value = proto.material_fluid.constant_density_value.value
