from inspect import Signature, signature
from typing import Any, Dict, List, Type, TypeVar, _GenericAlias  # type: ignore

from ..dtos import Registration
from ..enums import Scope
from ..helpers import ContainerHelpers, TypeHelpers
from ..interfaces import IScopeManager


class TransientScopeManager(IScopeManager):
    __base_types: List[Type]

    def __init__(self, base_types: List[Type]) -> None:
        self.__base_types = base_types

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.TRANSIENT

    def is_same_registration_scope_v2(
        self,
        interface: Type,
        child_interface: Type,
        container: Dict[Type, Registration],
    ) -> None:
        registration: Registration = container[child_interface]
        if registration.scope != Scope.TRANSIENT:
            error_message = f"Error Transient type: {TypeHelpers.to_string(interface)} registered with Singleton dependency: {TypeHelpers.to_string(child_interface)}"
            raise Exception(error_message)

    def resolve_scope_decorator(self, interface: Type, instance: Any) -> Any:
        return instance

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        return ContainerHelpers.resolve(
            interface=interface,
            container=container,
            is_same_registration_scope=self.is_same_registration_scope_v2,
            resolve_scope_decorator=self.resolve_scope_decorator,
            base_types=self.__base_types,
        )
