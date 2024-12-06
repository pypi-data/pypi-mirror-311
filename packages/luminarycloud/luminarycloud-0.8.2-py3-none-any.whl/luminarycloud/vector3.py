# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from ._proto.api.v0.luminarycloud.common import common_pb2 as commonpb
from ._proto.base.base_pb2 import AdVector3


@dataclass
class Vector3:
    """Represents a 3-dimensional vector."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def _to_proto(self) -> commonpb.Vector3:
        return commonpb.Vector3(x=self.x, y=self.y, z=self.z)

    def _from_proto(self, proto: commonpb.Vector3):
        self.x = proto.x
        self.y = proto.y
        self.z = proto.z

    def _to_ad_proto(self) -> AdVector3:
        advector = AdVector3()
        advector.x.value = self.x
        advector.y.value = self.y
        advector.z.value = self.z
        return advector

    def _from_ad_proto(self, proto: AdVector3):
        self.x = proto.x.value
        self.y = proto.y.value
        self.z = proto.z.value
