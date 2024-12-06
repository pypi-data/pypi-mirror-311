# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from collections.abc import Callable
from dataclasses import dataclass, field
from logging import getLogger
from os import PathLike
from typing import TypeVar, cast

from luminarycloud._helpers.cond import params_to_str
from luminarycloud._helpers.simulation_params_from_json import (
    simulation_params_from_json_path,
)
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud._proto.client.entity_pb2 import EntityIdentifier
from luminarycloud.params import _param_wrappers as w
from luminarycloud.params.convergence_criteria import ConvergenceCriteria
from luminarycloud.params.geometry import Volume
from luminarycloud.params.materials import Material
from luminarycloud.params.materials._proto import _material_from_proto
from luminarycloud.params.physics import Fluid, Physics
from luminarycloud.params.physics._proto import _physics_from_proto

logger = getLogger(__name__)

logger = getLogger(__name__)


@dataclass(kw_only=True, repr=False)
class SimulationParam(w.SimulationParam):
    """Simulation configuration that supports multiple physics."""

    materials: list[Material] = field(default_factory=list)
    "List of materials."
    physics: list[Physics] = field(default_factory=list)
    "List of physics solvers."
    convergence_criteria: ConvergenceCriteria = field(default_factory=ConvergenceCriteria)
    "Convergence criteria for the simulation."

    def _to_proto(self) -> clientpb.SimulationParam:
        _proto = super()._to_proto()
        _proto.material_entity.extend(m._to_proto() for m in self.materials)
        _proto.physics.extend(p._to_proto() for p in self.physics)
        _proto.convergence_criteria.CopyFrom(self.convergence_criteria._to_proto())
        return _proto

    @classmethod
    def from_proto(self, proto: clientpb.SimulationParam):
        _wrapper = cast(SimulationParam, super().from_proto(proto))
        _wrapper.materials = [_material_from_proto(v) for v in proto.material_entity]
        _wrapper.physics = [_physics_from_proto(v) for v in proto.physics]
        _wrapper.convergence_criteria = ConvergenceCriteria.from_proto(proto.convergence_criteria)
        return _wrapper

    @classmethod
    def from_json(cls, path: PathLike):
        return cls.from_proto(simulation_params_from_json_path(path))

    def assign_material(self, material: Material, volume: Volume | str):
        material_identifier = EntityIdentifier(id=material.id, name=material.name)
        if isinstance(volume, str):
            volume_identifier = EntityIdentifier(id=volume)
        else:
            volume_identifier = EntityIdentifier(id=volume.id, name=volume.name)

        volume_material_pairs = self.entity_relationships.volume_material_relationship
        _remove_from_list_with_warning(
            _list=volume_material_pairs,
            _accessor=lambda v: v.volume_identifier.id,
            _to_remove=volume_identifier.id,
            _warning_message=lambda v: f"Volume {_stringify_identifier(volume_identifier)} has already been assigned material {_stringify_identifier(v.material_identifier)}. Overwriting...",
        )

        if volume_identifier.id not in (v.volume_identifier.id for v in self.volume_entity):
            volume_entity = w.VolumeEntity(volume_identifier=volume_identifier)
            self.volume_entity.append(volume_entity)
        if material_identifier.id not in (m.id for m in self.materials):
            self.materials.append(material)

        volume_material_pairs.append(
            w.VolumeMaterialRelationship(
                volume_identifier=volume_identifier,
                material_identifier=material_identifier,
            )
        )

    def assign_physics(self, physics: Physics, volume: Volume | str):
        physics_identifier = EntityIdentifier(id=physics.id, name=physics.name)
        if isinstance(volume, str):
            volume_identifier = EntityIdentifier(id=volume)
        else:
            volume_identifier = EntityIdentifier(id=volume.id, name=volume.name)

        volume_physics_pairs = self.entity_relationships.volume_physics_relationship
        _remove_from_list_with_warning(
            _list=volume_physics_pairs,
            _accessor=lambda v: v.volume_identifier.id,
            _to_remove=volume_identifier.id,
            _warning_message=lambda v: f"Volume {_stringify_identifier(volume_identifier)} has already been assigned physics {_stringify_identifier(v.physics_identifier)}. Overwriting...",
        )
        if isinstance(physics, Fluid):
            _remove_from_list_with_warning(
                _list=volume_physics_pairs,
                _accessor=lambda v: v.physics_identifier.id,
                _to_remove=physics_identifier.id,
                _warning_message=lambda v: f"Fluid physics {_stringify_identifier(physics_identifier)} has already been assigned to volume {_stringify_identifier(v.volume_identifier)}. Overwriting...",
            )

        if volume_identifier.id not in (v.volume_identifier.id for v in self.volume_entity):
            self.volume_entity.append(w.VolumeEntity(volume_identifier=volume_identifier))
        if physics_identifier.id not in (p.id for p in self.physics):
            self.physics.append(physics)

        volume_physics_pairs.append(
            w.VolumePhysicsRelationship(
                volume_identifier=volume_identifier,
                physics_identifier=physics_identifier,
            )
        )

    def __repr__(self):
        return params_to_str(self._to_proto())


T = TypeVar("T")
U = TypeVar("U")


def _remove_from_list_with_warning(
    _list: list[T],
    _accessor: Callable[[T], U],
    _to_remove: U,
    _warning_message: Callable[[T], str],
) -> None:
    for i, e in reversed(list(enumerate(_list))):
        if _accessor(e) == _to_remove:
            logger.warning(_warning_message(e))
            _list.pop(i)


def _stringify_identifier(identifier: EntityIdentifier) -> str:
    if identifier.name:
        return f'"{identifier.name}" ({identifier.id})'
    else:
        return f"({identifier.id})"
