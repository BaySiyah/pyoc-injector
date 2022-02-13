import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import ioc


@dataclass
class DbConfiguration:
    host: str
    user: str
    password: str
    database: str


class DbConnector:

    configuration: DbConfiguration

    @ioc.inject
    def __init__(self, configuration: DbConfiguration, name: str = None) -> None:
        self.configuration = configuration
        self.name = name or "no name"

    def connect(self) -> None:
        print(">> open db connection (", end="")
        print(", ".join([f"{k}={v}" for k, v in vars(self.configuration).items()]), end="")
        print(")")

    def disconnect(self) -> None:
        print(">> close db connection")

    def __enter__(self) -> None:
        self.connect()

    def __exit__(self, type: type, ex: Exception, trace: traceback) -> None:
        self.disconnect()


class BaseRepository(ABC):

    connector: DbConnector

    @ioc.inject
    def __init__(self, connector: DbConnector) -> None:
        super().__init__()
        self.connector = connector

    @abstractmethod
    def get_data(self) -> Any:
        pass


class RepositoryA(BaseRepository):
    def get_data(self) -> list[str]:
        with self.connector:
            print(">> get data from repository A")
            return ["s", "m", "w", "k", "g"]


class RepositoryB(BaseRepository):
    def get_data(self) -> list[str]:
        with self.connector:
            print(">> get data from repository B")
            return ["e", "s", "o", "i", " "]


class RepositoryC(BaseRepository):
    def get_data(self) -> list[str]:
        with self.connector:
            print(">> get data from repository C")
            return ["e", " ", "r", "n", "!"]


class Service:

    repo_a: RepositoryA
    repo_b: RepositoryB
    repo_c: RepositoryC

    @ioc.inject
    def __init__(self, a: RepositoryA, b: RepositoryB, c: RepositoryC) -> None:
        self.repo_a = a
        self.repo_b = b
        self.repo_c = c

    def merge(self) -> None:
        a = self.repo_a.get_data()
        b = self.repo_b.get_data()
        c = self.repo_c.get_data()
        temp = []
        for x, y, z in zip(a, b, c):
            temp.append(x)
            temp.append(y)
            temp.append(z)
        temp = "".join(temp)
        print(f">> merge: {temp}")
