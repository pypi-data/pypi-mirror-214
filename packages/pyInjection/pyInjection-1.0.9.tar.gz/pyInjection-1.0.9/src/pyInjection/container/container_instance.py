from inspect import Signature, signature
from typing import Any, Dict, List, Type

from ..dtos import Registration
from ..enums import Scope
from ..helpers import TypeHelpers
from ..interfaces import IScopeManager, IValidator


class ContainerInstance:
    __container: Dict[Type, Registration]
    __validators: List[IValidator]
    __scope_managers: List[IScopeManager]
    __base_types: List[Type]
    __ignore_parameters: List[str]

    def __init__(
        self,
        validators: List[IValidator],
        scope_managers: List[IScopeManager],
        base_types: List[Type],
    ):
        self.__validators = validators
        self.__scope_managers = scope_managers
        self.__base_types = base_types
        self.__container = {}
        self.__ignore_parameters = ["self", "args", "kwargs"]

    def __is_valid(self, interface: Type, implementation: Any) -> bool:
        for validator in self.__validators:
            if not validator.is_valid(
                interface=interface, implementation=implementation
            ):
                return False
        return True

    def __add(self, interface: Type, implementation: Any, scope: Scope) -> None:
        error_message: str = ""
        if not interface in self.__container.keys():
            if self.__is_valid(interface=interface, implementation=implementation):
                self.__container[interface] = Registration(
                    implementation=implementation, scope=scope
                )
            else:
                error_message = f"Failed to add mapping '{TypeHelpers.to_string(interface)} -> {TypeHelpers.to_string(implementation)}' to the container"
                raise Exception(error_message)
        else:
            error_message = f"Cannot register a duplicate implementation for '{TypeHelpers.to_string(interface)}'"
            raise Exception(error_message)

    def add_transient(self, interface: Type, implementation: Any) -> None:
        self.__add(
            interface=interface, implementation=implementation, scope=Scope.TRANSIENT
        )

    def add_singleton(self, interface: Type, implementation: Any) -> None:
        self.__add(
            interface=interface, implementation=implementation, scope=Scope.SINGLETON
        )
        # check this resolves, need to write a new class that is not a
        # decorator and test that the resolve works

    def resolve(self, interface: Type) -> Any:
        if interface in self.__container.keys():
            scope = self.__container[interface].scope
            for scope_manager in self.__scope_managers:
                if scope_manager.can_resolve(scope=scope):
                    return scope_manager.resolve(
                        interface=interface, container=self.__container
                    )
        raise Exception("Cannot resolve type: {0}".format(str(interface)))

    def validate(self) -> None:
        for registration in self.__container.values():
            if type(registration.implementation) in self.__base_types:
                sig: Signature = signature(registration.implementation)
                for p in sig.parameters:
                    if p not in self.__ignore_parameters:
                        annotation: Any = sig.parameters[p].annotation
                        if not annotation in self.__container.keys():
                            raise Exception(
                                f"Missing registration for: '{TypeHelpers.to_string(annotation)}'"
                            )
