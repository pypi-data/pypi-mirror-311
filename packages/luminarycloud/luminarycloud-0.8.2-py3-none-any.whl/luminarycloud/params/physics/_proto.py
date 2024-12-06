# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params.physics.fluid import Fluid
from luminarycloud.params.physics.physics import Physics


def _physics_from_proto(proto: clientpb.Physics) -> Physics:
    if proto.HasField("fluid"):
        return Fluid.from_proto(proto)
    else:
        raise ValueError(f"Unknown material type: {proto}")
