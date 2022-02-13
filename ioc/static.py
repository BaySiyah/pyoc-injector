from typing import Type, TypeVar

from ioc.container import container

T = TypeVar("T")


def get_instance(type: Type[T]) -> T:
    return container.get_instance(type)


def instance_exists(type: type) -> bool:
    return container.instance_exists(type)
