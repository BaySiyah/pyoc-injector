import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import ioc
from data_access import DbConfiguration, DbConnector, RepositoryA, RepositoryB, RepositoryC, Service


def configure_ioc() -> None:
    config = DbConfiguration("localhost", "admin", "", "test_db")
    ioc.container.register_singleton(DbConfiguration, config)
    ioc.container.register_per_request(DbConnector, name="MYSQL")
    ioc.container.register_per_request(RepositoryA)
    ioc.container.register_per_request(RepositoryB)
    ioc.container.register_per_request(RepositoryC)
    ioc.container.register_per_request(Service)


def main() -> None:
    configure_ioc()
    service = ioc.get_instance(Service)
    service.merge()


if __name__ == "__main__":
    main()
