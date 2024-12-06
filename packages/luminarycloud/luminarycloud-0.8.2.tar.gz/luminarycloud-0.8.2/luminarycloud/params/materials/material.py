# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import abstractmethod
from dataclasses import dataclass, field
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud.params._param_wrappers import ParamGroupWrapper, create_unique_id


@dataclass(kw_only=True)
class Material(ParamGroupWrapper[clientpb.MaterialEntity]):
    id: str = field(init=False, default_factory=create_unique_id)
    name: str = ""

    @abstractmethod
    def _to_proto(self) -> clientpb.MaterialEntity:
        _proto = clientpb.MaterialEntity()
        _proto.material_identifier.id = self.id
        _proto.material_identifier.name = self.name
        return _proto

    @abstractmethod
    def _from_proto(self, proto: clientpb.MaterialEntity):
        self.name = proto.material_identifier.name
        self.id = proto.material_identifier.id
