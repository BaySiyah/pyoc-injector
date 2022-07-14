import setuptools


def readme():
    with open("README.md") as f:
        return f.read()

def license():
    with open("LICENSE") as f:
        return f.read()


setuptools.setup(
    name="ioc",
    version="0.1.0",
    description="A simple dependency injection module",
    long_description=readme(),
    author="BaySiyah",
    license=license(),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    zip_safe=False,
)
