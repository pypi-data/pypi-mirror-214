from inspect import Signature, signature
from logging import warning
from typing import Any, Dict, List, Type, _GenericAlias  # type: ignore

from ..dtos import Registration
from ..enums import Scope
from ..helpers import ContainerHelpers, TypeHelpers
from ..interfaces import IScopeManager


class SingletonScopeManager(IScopeManager):
    __resolved_instances: Dict[Type, Any]
    __base_types: List[Type]

    def __init__(self, base_types: List[Type]) -> None:
        self.__resolved_instances = {}
        self.__base_types = base_types

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.SINGLETON

    def is_same_registration_scope_v2(
        self,
        interface: Type,
        child_interface: Type,
        container: Dict[Type, Registration],
    ) -> None:
        registration: Registration = container[child_interface]
        if registration.scope != Scope.SINGLETON:
            warning_message: str = f"Warning Singleton type: {TypeHelpers.to_string(interface)} registered with Transient dependency: {TypeHelpers.to_string(child_interface)}"
            warning(warning_message)

    def resolve_scope_decorator(self, interface: Type, instance: Any) -> Any:
        if interface not in self.__resolved_instances.keys():
            self.__resolved_instances[interface] = instance
        return instance

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        if interface in self.__resolved_instances.keys():
            return self.__resolved_instances[interface]
        else:
            self.__resolved_instances[interface] = ContainerHelpers.resolve(
                interface=interface,
                container=container,
                is_same_registration_scope=self.is_same_registration_scope_v2,
                resolve_scope_decorator=self.resolve_scope_decorator,
                base_types=self.__base_types,
            )
            return self.__resolved_instances[interface]

    @property
    # Exposed for Unit Testing
    def resolved_instances(self) -> Dict[Type, Any]:
        return self.__resolved_instances
