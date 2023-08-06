from typing import Dict, Type, cast

from taipan_di.interfaces import BaseDependencyContainer, BaseDependencyProvider, BaseScope

from .dependency_provider import DependencyProvider

__all__ = ["DependencyContainer"]


class DependencyContainer(BaseDependencyContainer):
    def __init__(self) -> None:
        self._services = cast(Dict[Type, BaseScope], {})

    def contains(self, type: Type) -> bool:
        return type in self._services

    def register(self, type: Type, service: BaseScope) -> None:
        self._services[type] = service

    def build(self) -> BaseDependencyProvider:
        provider = DependencyProvider(self._services)
        return provider
