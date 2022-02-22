from typing import Type, TypeVar

from ioc.container import container

T = TypeVar("T")

def register(type: type, **kwds) -> None:
    container.register_per_request(type, **kwds)

def register_singleton(type: type, instance: object = None) -> None:
    container.register_singleton(type, instance)

def get(type: Type[T]) -> T:
    return container.get_instance(type)


def exists(type: type) -> bool:
    return container.instance_exists(type)
