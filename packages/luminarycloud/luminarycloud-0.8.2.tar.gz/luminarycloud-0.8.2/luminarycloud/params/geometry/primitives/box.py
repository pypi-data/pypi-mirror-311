# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud.params.geometry.geometry import Volume, Surface, GeometryEntity


class Box(Volume):
    front: Surface
    back: Surface
    left: Surface
    right: Surface
    top: Surface
    bottom: Surface

    def __init__(self, name: str):
        self.name = name

    def create_around(self, entity: GeometryEntity, **kwargs):
        pass
