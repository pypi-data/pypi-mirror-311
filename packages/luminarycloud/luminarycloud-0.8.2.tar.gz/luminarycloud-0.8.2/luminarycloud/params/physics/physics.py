# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass, field
from luminarycloud.params._param_wrappers import ParamGroupWrapper, create_unique_id
from luminarycloud._proto.client import simulation_pb2 as clientpb


@dataclass(kw_only=True)
class Physics(ParamGroupWrapper[clientpb.Physics]):
    """Physics configuration for a simulation."""

    id: str = field(init=False, default_factory=create_unique_id)
    "Unique identifier for a physics entity"
    name: str = ""

    @abstractmethod
    def _to_proto(self) -> clientpb.Physics:
        _proto = clientpb.Physics()
        _proto.physics_identifier.id = self.id
        _proto.physics_identifier.name = self.name
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.Physics):
        self.id = proto.physics_identifier.id
