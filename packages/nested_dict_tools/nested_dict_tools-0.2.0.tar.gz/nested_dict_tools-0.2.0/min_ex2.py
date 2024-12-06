from collections.abc import Callable, Mapping
from typing import Any, Protocol, overload

type NestedMapping[K, V] = Mapping[K, NestedMappingNode[K, V]]
type NestedMappingNode[K, V] = V | NestedMapping[K, V]


type NestedMapping2[K, V] = Mapping[K, NestedMapping2[K, V]]


class CallableArbitraryNbArgs(Protocol):
    """Protocol for a callable that accepts an arbitrary number of arguments."""

    def __call__(self, *args: Any) -> Any: ...  # noqa: D102


# === With NestedMapping: false positive ===
@overload
def map_leaves_1[K, V, W](
    func: CallableArbitraryNbArgs,
    *nested_dicts: NestedMapping[K, V],
) -> NestedMapping[K, W]: ...


# Overload 2 for "map_leaves_no_generic_protocol" will never be used because its parameters overlap overload 1
@overload
def map_leaves_1[K, W](
    func: Callable[..., W],
    *nested_dicts: NestedMapping[K, Any],
) -> NestedMapping[K, W]: ...


def map_leaves_1[K, W](
    func: Callable[..., W] | CallableArbitraryNbArgs, *nested_dicts: NestedMapping[K, Any]
) -> NestedMapping[K, W]:
    del nested_dicts
    del func
    raise NotImplementedError


# === With NestedMapping2: no error ===
@overload
def map_leaves_2[K, V, W](
    func: CallableArbitraryNbArgs,
    *nested_dicts: NestedMapping2[K, V],
) -> NestedMapping[K, W]: ...


@overload
def map_leaves_2[K, W](
    func: Callable[..., W],
    *nested_dicts: NestedMapping2[K, Any],
) -> NestedMapping[K, W]: ...


def map_leaves_2[K, W](
    func: Callable[..., W] | CallableArbitraryNbArgs, *nested_dicts: NestedMapping2[K, Any]
) -> NestedMapping[K, W]:
    del nested_dicts
    del func
    raise NotImplementedError
