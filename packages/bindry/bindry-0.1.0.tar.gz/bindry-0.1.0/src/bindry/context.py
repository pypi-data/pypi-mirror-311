import inspect
from typing import List, Optional

from .config import DependencyConfiguration
from .exceptions import DependencyInjectionException
from .loader import ConfigurationLoader
from .scope import Scope


class ApplicationContext:
    """
    Manages the dependency injection lifecycle for components and beans.
    Supports profile-based configurations and both singleton and prototype scopes.
    """

    _instance = None  # Singleton instance

    def __init__(self):
        """
        Initializes the application context with a default configuration and component registry.
        """
        if not hasattr(self, "ioc_compoment_instances"):
            self.ioc_compoment_instances = {}

    @classmethod
    def get_instance(cls) -> "ApplicationContext":
        """
        Retrieves the singleton instance of the ApplicationContext.

        Returns:
            ApplicationContext: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = ApplicationContext()
        return cls._instance

    def load_configuration(
        self,
        file_path: str,
        base_env_file: str = ".env",
        active_profiles: Optional[List[str]] = None,
    ):
        """
        Load configuration from YAML or JSON file with multi-profile .env support

        Args:
            file_path: Path to the configuration file
            base_env_file: Base .env file name
            active_profiles: List of active profiles
        """
        ConfigurationLoader.load_configuration(
            file_path, base_env_file, active_profiles
        )

    def set_active_profiles(self, profiles: List[str]):
        """
        Sets the active profiles, ensuring the 'default' profile is always at the beginning.

        Args:
            profiles (List[str]): List of profiles to set as active.
        """
        dependency_configuration = DependencyConfiguration().get_instance()
        dependency_configuration.set_active_profiles(profiles)

    def get_bean(self, cls):
        """
        Retrieves an instance of the requested component class, considering profiles and scopes.

        Args:
            cls (Type): The class of the bean to retrieve.

        Returns:
            Any: An instance of the requested bean.

        Raises:
            DependencyInjectionException: If the requested bean cannot be found or instantiated.
        """
        dependency_configuration = DependencyConfiguration().get_instance()

        # Get class name
        class_name = cls.__name__

        # Check active profiles in reverse order (later profiles override earlier ones)
        bean_definition = None
        for profile in reversed(dependency_configuration.active_profiles):
            profile_config = dependency_configuration.profiles.get(profile)
            if profile_config and class_name in profile_config.bean_definitions:
                bean_definition = profile_config.bean_definitions[class_name]
                break

        if bean_definition:
            bean_cls = bean_definition.implementation_class
            scope = bean_definition.scope
            constructor_args = bean_definition.constructor_args
        else:
            raise DependencyInjectionException(
                f"Bean for class '{class_name}' not found in any active profile"
            )

        # Handle Singleton Scope
        if scope == Scope.SINGLETON and bean_cls in self.ioc_compoment_instances:
            return self.ioc_compoment_instances[bean_cls]

        # Get constructor signature
        try:
            constructor = inspect.signature(bean_cls.__init__)
            params = constructor.parameters
        except (DependencyInjectionException, AttributeError):
            instance = bean_cls()
            if scope == Scope.SINGLETON:
                self.ioc_compoment_instances[bean_cls] = instance
            return instance

        dependencies = []
        kwargs = {}
        varargs = []

        # First, collect any kwargs specified in constructor_args
        if "kwargs" in constructor_args:
            kwargs.update(constructor_args["kwargs"])

        # Handle different parameter kinds
        for param_name, param in list(params.items())[1:]:  # Skip 'self'
            # Handle *args
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                if "args" in constructor_args:
                    varargs.extend(constructor_args["args"])
                continue
            # Handle **kwargs
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                # Any remaining constructor_args that aren't handled elsewhere
                # and aren't special keys ('args', 'kwargs') go into kwargs
                for key, value in constructor_args.items():
                    if key not in ["args", "kwargs"] and key not in params:
                        kwargs[key] = value
                continue
            # Handle normal parameters
            else:
                if param_name in constructor_args:
                    if param.kind == inspect.Parameter.KEYWORD_ONLY:
                        kwargs[param_name] = constructor_args[param_name]
                    else:
                        dependencies.append(constructor_args[param_name])
                elif param.annotation != inspect._empty:
                    dependency = self.get_bean(param.annotation)
                    if param.kind == inspect.Parameter.KEYWORD_ONLY:
                        kwargs[param_name] = dependency
                    else:
                        dependencies.append(dependency)
                elif param.default != inspect.Parameter.empty:
                    if param.kind == inspect.Parameter.KEYWORD_ONLY:
                        kwargs[param_name] = param.default
                    else:
                        dependencies.append(param.default)
                else:
                    raise DependencyInjectionException(
                        f"Cannot resolve parameter '{param_name}' for class '{class_name}'"
                    )

        # Merge dependencies and varargs
        all_args = [*dependencies, *varargs]

        # Instantiate the bean
        try:
            instance = bean_cls(*all_args, **kwargs)
        except TypeError as e:
            # If instantiation fails, try with just kwargs
            instance = bean_cls(**kwargs)

        self._initialize_autowired_methods(instance)

        # Save singleton instances
        if scope == Scope.SINGLETON:
            self.ioc_compoment_instances[bean_cls] = instance

        return instance

    def _initialize_autowired_methods(self, instance):
        """
        Initializes methods decorated with @autowired in a component.

        Args:
            instance (Any): The component instance to initialize.
        """
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            # If method has _is_autowired attribute, call it to inject dependencies
            if getattr(method, "_is_autowired", False):
                wrapper = method
                wrapper(_ioc_application_context_=self)
