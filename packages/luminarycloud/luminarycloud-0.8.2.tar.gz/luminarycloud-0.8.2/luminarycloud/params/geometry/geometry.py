# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass, field

from luminarycloud.params._param_wrappers import create_unique_id


@dataclass
class GeometryEntity:
    id: str = field(default_factory=create_unique_id, init=False)
    name: str


@dataclass
class Volume(GeometryEntity):
    pass


@dataclass
class Surface(GeometryEntity):
    pass


class Geometry:
    def select(self, tag_name):
        pass

    def add(self, entity: GeometryEntity):
        pass
