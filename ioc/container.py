from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Type, TypeVar


@dataclass
class BaseEntry(ABC):
    """Base class of all entry types."""

    entry_type: type

    @abstractmethod
    def get(self) -> object:
        """Returns an instance of the registered entry type."""


@dataclass
class SingletonEntry(BaseEntry):
    """A singlton entry. Returns always the same instance of an object."""

    _instance: object = None

    def get(self) -> object:
        if not self._instance:
            self._instance = self.entry_type()
        return self._instance


@dataclass
class PerRequestEntry(BaseEntry):
    """Returns always a new instance."""

    arguments: tuple = field(default_factory=tuple)
    keywords: dict[str, Any] = field(default_factory=dict)

    def get(self) -> object:
        return self.entry_type(*self.arguments, **self.keywords, __from_ioc__=True)


T = TypeVar("T")


class Container(ABC):

    _entries: dict[type, BaseEntry]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Removes all registered types from the container."""
        self._entries = {}

    def get_instance(self, type: Type[T]) -> T:
        """Returns the given type from the container."""
        if not self.type_exists(type):
            raise Exception(f"type '{type.__name__}' is not registered")
        return self._entries[type].get()

    def type_exists(self, type: type) -> bool:
        """Returns true if the type is registered."""
        return type in self._entries

    def _register(self, entry: BaseEntry) -> None:
        if entry.entry_type in self._entries:
            raise Exception(f"type '{entry.entry_type.__name__}' already exists")
        self._entries[entry.entry_type] = entry

    def register_per_request(self, type: type, *args, **kwds) -> None:
        """Register a type per request. You can specify default arguments for the constructor."""
        entry = PerRequestEntry(type, args, kwds)
        self._register(entry)

    def register_singleton(self, type: type, instance: object = None) -> None:
        """Register a singleton type."""
        entry = SingletonEntry(type, instance)
        self._register(entry)


container: Container = Container()
