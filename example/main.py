import ioc
from data_access import DbConfiguration, DbConnector, RepositoryA, RepositoryB, RepositoryC, Service


def configure_ioc() -> None:
    config = DbConfiguration("localhost", "admin", "", "test_db")
    ioc.register_singleton(DbConfiguration, config)
    ioc.register(DbConnector, name="MYSQL")
    ioc.register(RepositoryA)
    ioc.register(RepositoryB)
    ioc.register(RepositoryC)
    ioc.register(Service)


def main() -> None:
    configure_ioc()
    service = ioc.get(Service)
    service.merge()


if __name__ == "__main__":
    main()
