import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union, cast

from .config import DependencyConfiguration
from .exceptions import DependencyInjectionException


def component(
    scope: str,
    bean_type: Optional[Type] = None,
    profile: Union[str, List[str]] = "default",
    constructor_args: Optional[Dict[str, Any]] = None,
):
    """
    Enhanced component decorator that supports bean_type specification and constructor arguments.

    Args:
        scope (str): Component lifecycle scope (e.g., 'singleton', 'prototype')
        bean_type (Optional[Type]): Optional bean_type/base class that this component implements
        profile (Union[str, List[str]]): Profile(s) under which to register the component
        constructor_args (Optional[Dict[str, Any]]): Optional constructor arguments for the component

    Examples:
        @component(Scope.SINGLETON)
        class SimpleService:
            pass

        @component(Scope.SINGLETON, bean_type=IMessageService)
        class EmailService(IMessageService):
            pass

        @component(
            scope=Scope.SINGLETON,
            bean_type=IDataService,
            constructor_args={"timeout": 30}
        )
        class DatabaseService(IDataService):
            def __init__(self, timeout: int):
                self.timeout = timeout
    """

    def decorator(cls: Type):
        dependency_configuration = DependencyConfiguration().get_instance()

        # Handle both single profile string and list of profiles
        profiles = [profile] if isinstance(profile, str) else profile

        # Register component for each specified profile
        for p in profiles:
            # If bean_type is provided, use register_bean
            if bean_type is not None:
                dependency_configuration.register_bean(
                    bean_type=bean_type,
                    implementation_class=cls,
                    scope=scope,
                    constructor_args=constructor_args,
                    profile=p,
                )
            else:
                # If no bean_type specified, use the class itself as both bean_type and implementation
                dependency_configuration.register_bean(
                    bean_type=cls,
                    implementation_class=cls,
                    scope=scope,
                    constructor_args=constructor_args,
                    profile=p,
                )
        return cls

    return decorator


def autowired(method):
    """
    Decorator to automatically inject dependencies into a method.

    Dependencies are resolved using the application's Dependency Injection context.

    Raises:
        DependencyInjectionException: If a parameter is missing a type annotation.
    """

    def wrapper(self, *args, **kwargs):
        if "_ioc_application_context_" not in kwargs:
            # Call the original method with the original args
            return method(self, *args, **kwargs)

        context = kwargs["_ioc_application_context_"]
        del kwargs["_ioc_application_context_"]
        dependencies = []

        # Inspect the parameters for type annotations
        for param in inspect.signature(method).parameters.values():
            # Skip 'self' parameter
            if param.name == "self":
                continue
            if param.annotation == inspect._empty:
                raise DependencyInjectionException(
                    f"Parameter '{param.name}' must have a type annotation"
                )

            # Fetch the bean by class (annotation) from ApplicationContext
            dependency = context.get_bean(param.annotation)
            dependencies.append(dependency)

        # Call the original method with the resolved dependencies
        return method(self, *dependencies, **kwargs)

    # Mark this method as autowired
    wrapper_with_attr = cast(Callable[[Any, Any], Any], wrapper)
    wrapper_with_attr._is_autowired = True  # type: ignore
    return wrapper_with_attr
