# pyoc-injector
A simple dependency injection module.

## container configuration

Before the injector is able to inject the dependencies you have to configure the container. The examples below shows how you register types.
```py
import ioc

class Foo:
    ...
class Bar:
    ...

# Register a type
ioc.register(Foo)

# Register a type with keyword arguments
ioc.register(Foo, name="James", age=42)

# Register a singleton type
ioc.register_singleton(Bar)

# Register a singlton instance
bar = Bar()
ioc.register_singleton(Bar, bar)
# or
ioc.register_singleton(type(bar), bar)
```

## get instance from container

To get the instances directly from the container you can simply call the ```get``` method.

```py
import ioc

class Foo:
    ...

ioc.register(Foo)
foo = ioc.get(Foo)
```

The ```foo``` object will be injected from the container.

## the ```inject``` decorator

Use the ```@ioc.inject``` decorator above the ```__init__``` method to inject the ```bar``` object from the container.

```py
import ioc

class Foo:
    ...

class Bar:
    @ioc.inject
    def __init__(foo: Foo) -> None:
        ...

    def say_hello() -> None:
        print("Hello!")

ioc.register(Foo)
ioc.register(Bar)

bar = ioc.get(Bar)
bar.say_hello()

```
