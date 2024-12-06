# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import ABC
from enum import Enum
from typing import (
    cast,
    Any,
    Generic,
    Optional,
    TypeVar,
    NewType,
    get_type_hints,
    get_origin,
    get_args,
)

from google.protobuf.message import Message


# We mainly need this to statically declare to the linter that these
# attributes will eventually exist.
class ProtoWrapperBase(ABC):
    _proto: Message

    def __init__(self, proto_type: Optional[Message] = None):
        pass


P = TypeVar("P", bound=Message)
C = TypeVar("C", bound=ProtoWrapperBase)


class ProtoWrapper(Generic[P]):
    def __init__(decorator, proto_type: type[P]):
        decorator.proto_type = proto_type

    def __call__(decorator, cls: type[C]) -> type[C]:
        class _W(cls):  # type: ignore
            def __init__(self, proto: Optional[P] = None):
                if proto is None:
                    proto = decorator.proto_type()
                self._proto = cast(P, proto)

            def __str__(self) -> str:
                return self._proto.__str__()

            def __repr__(self) -> str:
                return self._proto.__repr__()

        # This binds the field name to the getter.
        def getter(field_name: str) -> Any:
            return lambda self: getattr(self._proto, field_name)

        def wrapped_getter(field_name: str, wrapper: type[ProtoWrapperBase]) -> Any:
            return lambda self: wrapper(getattr(self._proto, field_name))

        # This binds the field name to the setter.
        def setter(field_name: str):
            return lambda self, value: setattr(self._proto, field_name, value)

        def wrapped_setter(field_name: str, wrapper: type[ProtoWrapperBase]):
            def _set(self, value):
                if not isinstance(value, wrapper):
                    raise TypeError(f"{field_name} should be a {wrapper.__name__}")
                setattr(self._proto, field_name, value._proto)

            return _set

        def list_wrapped_getter(field_name: str, wrapper: type[ProtoWrapperBase]) -> Any:
            return lambda self: RepeatedProtoWrapper(wrapper, getattr(self._proto, field_name))

        def list_wrapped_setter(field_name: str, wrapper: type[ProtoWrapperBase]) -> Any:
            def _set(self, values):
                for value in values:
                    if not isinstance(value, wrapper):
                        raise TypeError(f"{field_name} should be a list of {wrapper.__name__}")
                setattr(self._proto, field_name, [value._proto for value in values])

            return _set

        # Create getters that access the attributes of the underlying proto.
        type_hints = get_type_hints(cls)
        for field in decorator.proto_type.DESCRIPTOR.fields:
            _type = type_hints.get(field.name, None)
            if _type:
                fget = getter(field.name)
                fset = setter(field.name)
                _origin_type = get_origin(_type)
                if _origin_type is list:
                    _listed_type = get_args(_type)[0]
                    if issubclass(_listed_type, Enum) or issubclass(_listed_type, ProtoWrapperBase):
                        fget = list_wrapped_getter(field.name, _listed_type)
                        fset = None
                elif isinstance(_type, NewType):
                    pass
                elif issubclass(_type, Enum) or issubclass(_type, ProtoWrapperBase):
                    fget = wrapped_getter(field.name, _type)
                    fset = wrapped_setter(field.name, _type)
                setattr(_W, field.name, property(fget=fget, fset=fset))

        # Rename the wrapped class.
        _W.__name__ = cls.__name__

        return cast(type[C], _W)


class RepeatedProtoWrapper(Generic[C]):
    def __init__(self, wrapper: type[C], values: list[C]):
        self._wrapper = wrapper
        self._values = values

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        return self._wrapper(self._values[key])

    def __setitem__(self, key, value: C):
        if not isinstance(value, self._wrapper):
            raise TypeError
        self._values[key] = value._proto

    def __delitem__(self, key):
        del self._values[key]

    def __iter__(self):
        return (self._wrapper(value) for value in self._values)

    def __reversed__(self):
        return reversed(self.__iter__())

    def append(self, value: C):
        if not isinstance(value, self._wrapper):
            raise TypeError
        self._values.append(value._proto)
