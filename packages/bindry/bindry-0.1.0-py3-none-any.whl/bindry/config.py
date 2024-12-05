from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type


@dataclass
class ProfileConfig:
    """
    Represents configuration for a specific profile in the Dependency Injection system.

    Attributes:
        name (str): Name of the profile.
        bean_definitions (dict): Bean definitions for the profile.
    """

    name: str
    bean_definitions: Dict[str, "BeanDefinition"]


class BeanDefinition:
    """
    Represents a definition of a Dependency Injection-managed bean.

    Attributes:
        implementation_class (Type): The class implementing the bean.
        scope (str): The lifecycle scope of the bean.
        constructor_args (Optional[dict]): Constructor arguments for the bean.
    """

    def __init__(
        self,
        implementation_class: Type,
        scope: str,
        constructor_args: Optional[Dict[str, Any]] = None,
    ):
        self.implementation_class = implementation_class
        self.scope = scope
        self.constructor_args = constructor_args or {}


class DependencyConfiguration:
    """
    Configuration object that manages active profiles and explicitly defined beans.
    """

    _instance = None

    def __init__(self):
        """
        Initializes the DependencyConfiguration with default settings.
        """
        self.profiles: Dict[str, ProfileConfig] = {
            "default": ProfileConfig("default", {})
        }
        self.active_profiles: List[str] = ["default"]

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the DependencyConfiguration.

        Returns:
            DependencyConfiguration: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = DependencyConfiguration()
        return cls._instance

    def set_active_profiles(self, profiles: List[str]):
        """
        Sets the active profiles, ensuring the 'default' profile is always at the beginning.

        Args:
            profiles (List[str]): List of profiles to set as active.
        """
        # Remove 'default' if it exists in the profiles list
        filtered_profiles = [p for p in profiles if p != "default"]
        # Add 'default' at the beginning
        self.active_profiles = ["default"] + filtered_profiles

    def get_active_profiles(self) -> List[str]:
        """
        Retrieves the list of active profiles.

        Returns:
            List[str]: A copy of the active profiles.
        """
        return self.active_profiles.copy()

    def register_bean(
        self,
        bean_type: Type,
        implementation_class: Type,
        scope: str,
        constructor_args: Optional[Dict[str, Any]] = None,
        profile: str = "default",
    ):
        """
        Registers a bean (component) in the configuration or via decorator.

        Args:
            bean_type (Type): The bean_type or base class of the bean.
            implementation_class (Type): The concrete implementation class of the bean.
            scope (str): The lifecycle scope of the bean (e.g., SINGLETON, PROTOTYPE).
            constructor_args (Optional[Dict[str, Any]]): Arguments for the bean constructor.
            profile (str): The profile under which this bean is registered.
        """
        if profile not in self.profiles:
            self.profiles[profile] = ProfileConfig(profile, {})

        self.profiles[profile].bean_definitions[bean_type.__name__] = BeanDefinition(
            implementation_class=implementation_class,
            scope=scope,
            constructor_args=constructor_args,
        )
