from inspect import Signature, signature
from typing import (  # type: ignore
    Any,
    Callable,
    Dict,
    List,
    Type,
    TypeVar,
    _GenericAlias,
)

from ..dtos import Registration
from .type_helpers import TypeHelpers


class ContainerHelpers:
    ignore_parameters: List[str] = ["self", "args", "kwargs"]

    @staticmethod
    def resolve(
        interface: Type,
        container: Dict[Type, Registration],
        is_same_registration_scope: Callable,
        resolve_scope_decorator: Callable[[Type, Any], Any],
        base_types: List[Type],
    ) -> Any:
        error_message: str = ""
        if interface in container.keys():
            implementation: Any = container[interface].implementation
            if type(implementation) in base_types:
                if type(implementation) == _GenericAlias:  # type: ignore
                    return resolve_scope_decorator(
                        interface,
                        ContainerHelpers.resolve_generic(
                            interface=interface,
                            container=container,
                            is_same_registration_scope=is_same_registration_scope,
                            resolve_scope_decorator=resolve_scope_decorator,
                            base_types=base_types,
                        ),
                    )
                else:
                    kwargs: Any = {}
                    sig: Signature = signature(implementation)
                    for p in sig.parameters:
                        if p not in ContainerHelpers.ignore_parameters:
                            child_interface: Type = sig.parameters[p].annotation
                            is_same_registration_scope(
                                interface=interface,
                                child_interface=child_interface,
                                container=container,
                            )
                            instance = resolve_scope_decorator(
                                child_interface,
                                ContainerHelpers.resolve(
                                    interface=child_interface,
                                    container=container,
                                    is_same_registration_scope=is_same_registration_scope,
                                    resolve_scope_decorator=resolve_scope_decorator,
                                    base_types=base_types,
                                ),
                            )
                            kwargs[p] = instance
                    return implementation(**kwargs)
            elif type(implementation) == type(lambda: ""):
                return implementation()
            else:
                return implementation
        else:
            error_message = f"Cannot resolve type: {TypeHelpers.to_string(interface)}"
            raise Exception(error_message)

    @staticmethod
    def resolve_generic(
        interface: Type,
        container: Dict[Type, Registration],
        is_same_registration_scope: Callable,
        resolve_scope_decorator: Callable[[Type, Any], Any],
        base_types: List[Type],
    ) -> Any:
        replace_child_type: bool = False
        implementation: Any = container[interface].implementation
        implementation_type: Type = implementation.__origin__
        generic_class: Type = implementation.__args__[0]
        kwargs: Any = {}
        sig: Signature = signature(implementation_type)
        for p in sig.parameters:
            if p not in ContainerHelpers.ignore_parameters:
                child_interface: Type = sig.parameters[p].annotation
                if type(child_interface) == _GenericAlias:  # type: ignore
                    child_interface_generic_type = child_interface.__args__[0]
                    if type(child_interface_generic_type) == TypeVar:
                        ## Generic type needs to be passed down from parent
                        child_interface.__args__ = (generic_class,)
                        replace_child_type = True
                is_same_registration_scope(
                    interface=interface,
                    child_interface=child_interface,
                    container=container,
                )
                instance = resolve_scope_decorator(
                    child_interface,
                    ContainerHelpers.resolve(
                        interface=child_interface,
                        container=container,
                        is_same_registration_scope=is_same_registration_scope,
                        resolve_scope_decorator=resolve_scope_decorator,
                        base_types=base_types,
                    ),
                )
                kwargs[p] = instance
                ## Place TypeVar back into child_interface for later resolves
                if replace_child_type:
                    T = TypeVar("T")
                    child_interface.__args__ = (T,)
        return implementation(**kwargs)
