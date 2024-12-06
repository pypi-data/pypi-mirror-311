# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._proto.client import simulation_pb2 as clientpb
import luminarycloud.params.enum as enum
from luminarycloud.params.materials.fluid import ConstantDensity, ConstantDensityEnergy, IdealGas


def _material_from_proto(proto: clientpb.MaterialEntity):
    if proto.HasField("material_fluid"):
        if proto.material_fluid.density_relationship == enum.DensityRelationship.CONSTANT_DENSITY:
            return ConstantDensity.from_proto(proto)
        elif (
            proto.material_fluid.density_relationship
            == enum.DensityRelationship.CONSTANT_DENSITY_ENERGY
        ):
            return ConstantDensityEnergy.from_proto(proto)
        elif proto.material_fluid.density_relationship == enum.DensityRelationship.IDEAL_GAS:
            return IdealGas.from_proto(proto)
        else:
            raise ValueError(f"Unknown material fluid type: {proto}")
    else:
        raise ValueError(f"Unknown material type: {proto}")
