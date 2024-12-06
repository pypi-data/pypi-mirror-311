"""Ok."""

from collections.abc import Callable, Mapping
from typing import Any, Protocol, overload

type NestedMapping[K, V] = Mapping[K, NestedMappingNode[K, V]]
type NestedMappingNode[K, V] = V | NestedMapping[K, V]


class CallableArbitraryNbArgs[T, R](Protocol):
    """Protocol for a callable that accepts an arbitrary number of arguments of a given type."""

    def __call__(self, *args: T) -> R: ...  # noqa: D102


class CallableArbitraryNbArgsNoGeneric(Protocol):
    """Protocol for a callable that accepts an arbitrary number of arguments of a given type."""

    def __call__(self, *args: Any) -> Any: ...  # noqa: D102


@overload
def map_leaves[K, V, W](
    func: CallableArbitraryNbArgs[K, W],
    *nested_dicts: NestedMapping[K, V],
) -> NestedMapping[K, W]: ...


@overload
def map_leaves[K, W](
    func: Callable[..., W],
    *nested_dicts: NestedMapping[K, Any],
) -> NestedMapping[K, W]: ...


def map_leaves[K, W](
    func: Callable[..., W] | CallableArbitraryNbArgs[K, W], *nested_dicts: NestedMapping[K, Any]
) -> NestedMapping[K, W]:
    del nested_dicts
    del func
    raise NotImplementedError


@overload
def map_leaves_no_generic_protocol[K, V, W](
    func: CallableArbitraryNbArgsNoGeneric,
    *nested_dicts: NestedMapping[K, V],
) -> NestedMapping[K, W]: ...


@overload
def map_leaves_no_generic_protocol[K, W](
    func: Callable[..., W],
    *nested_dicts: NestedMapping[K, Any],
) -> NestedMapping[K, W]: ...


def map_leaves_no_generic_protocol[K, W](
    func: Callable[..., W] | CallableArbitraryNbArgsNoGeneric, *nested_dicts: NestedMapping[K, Any]
) -> NestedMapping[K, W]:
    del nested_dicts
    del func
    raise NotImplementedError


@overload
def map_leaves_mapping[K, V, W](
    func: CallableArbitraryNbArgs[K, W],
    *nested_dicts: Mapping[K, V],
) -> NestedMapping[K, W]: ...


@overload
def map_leaves_mapping[K, W](
    func: Callable[..., W],
    *nested_dicts: Mapping[K, Any],
) -> NestedMapping[K, W]: ...


def map_leaves_mapping[K, W](
    func: Callable[..., W] | CallableArbitraryNbArgs[K, W], *nested_dicts: Mapping[K, Any]
) -> NestedMapping[K, W]:
    del nested_dicts
    del func
    raise NotImplementedError
