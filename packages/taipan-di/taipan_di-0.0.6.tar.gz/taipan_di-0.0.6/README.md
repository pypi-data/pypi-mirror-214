# Taipan-DI

Truly Amazing Inversion of control Python library Analogous to .Net's DI

Taipan-DI is a [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection) library whose goal is to provide a behaviour similar to [.Net's DI system](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection).


## Features

 - Lightweight
 - No decorators
 - No hidden behaviour (what you write is what you get)
 - Automatic dependency injection on service resolving
 - Type hinting
 - No global container by default
 - Singleton and factory scopes
 - Register pipelines easily


## Constraints

 - Based purely on types (not on strings)
 - No automatic registration
 - It is necessary to write an `__init__` function or use `@dataclass`


## Installation

### Pip

> `pip install taipan-di`

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

> `poetry add taipan-di`


## Usage

First, you have to create a `DependencyCollection` in which you will register your services. Each `DependencyCollection` is independant and contain different services.

> `services = DependencyCollection()`

Then, register your services as you wish. They can be registered as factories or singletons using the following methods :

 - `services.register_factory(InterfaceType, ImplementationType)`
 - `services.register_singleton(InterfaceType, ImplementationType)`

You can also provide a creator method or an instance (for singletons only) that will be used when resolving the services :

 - `services.register_factory_creator(Type, lambda provider: create(provider))`
 - `services.register_singleton_creator(Type, lambda provider: create(provider))`
 - `services.register_singleton_instance(Type, instance)`

You can also register pipelines. Examples are given in the test files.

Once your services are registered, you have to build a dependency provider which will be used to resolve services : 

> `provider = services.build()`<br/>
> `resolved = provider.resolve(InterfaceType)`

If `ImplementationType` has a constructor dependency, it will be automatically resolved, as long as the dependency has been registered in the `DependencyCollection`.


## Inspirations

This library is partially based on the [*kink*](https://pypi.org/project/kink/) dependency injection library. I was using kink on another project previously but it didn't fit all my requirements.

I also took inspiration from the [*injector*](https://pypi.org/project/injector/) library and .Net's dependency injection system.


## TODO

This library isn't stable yet and a lot of things can still be improved.
If there is something you want to see added or if something does not work as you want it to, feel free to open an issue.

Here is a list of features I have in mind and will be working on :

 - Modify the registration process / methods to better handle type conditions and protocols
 - Create configuration from environment or configuration files

