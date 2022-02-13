from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type, TypeVar


@dataclass
class BaseEntry(ABC):

    type: type

    def create_instance(self, *args, **kwds) -> object:
        kwds["__from_ioc__"] = True
        return self.type(*args, **kwds)

    @abstractmethod
    def get(self) -> object:
        ...


class SingletonEntry(BaseEntry):

    _instance: object

    def __init__(self, type: type, instance: object = None) -> None:
        super().__init__(type)
        self._instance = instance

    def get(self) -> object:
        if not self._instance:
            self._instance = self.create_instance()
        return self._instance


class PerRequestEntry(BaseEntry):

    _keyword_args: dict[str, Any]

    def __init__(self, type: type, **kwargs) -> None:
        super().__init__(type)
        self._keyword_args = kwargs

    def get(self) -> object:
        return self.create_instance(**self._keyword_args)


T = TypeVar("T")


class Container(ABC):

    _entries: dict[type, BaseEntry]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._entries = {}

    def get_instance(self, type: Type[T]) -> T:
        if not self.instance_exists(type):
            raise Exception(f"type '{type.__name__}' is not registered")
        return self._entries[type].get()

    def instance_exists(self, type: type) -> bool:
        return type in self._entries

    def _register(self, entry: BaseEntry) -> None:
        if entry.type in self._entries:
            raise Exception(f"type '{entry.type.__name__}' already exists")
        self._entries[entry.type] = entry

    def register_singleton(self, type: type, instance: object = None) -> None:
        self._register(SingletonEntry(type, instance))

    def register_per_request(self, type: type, **kwargs) -> None:
        self._register(PerRequestEntry(type, **kwargs))


container: Container = Container()
