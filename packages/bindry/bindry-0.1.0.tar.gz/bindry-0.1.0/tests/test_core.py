from unittest.mock import MagicMock, patch

import pytest

from bindry.config import BeanDefinition, DependencyConfiguration
from bindry.exceptions import DependencyInjectionException
from bindry.scope import Scope


def test_scope_constants():
    """Test that Scope class has correct constant values"""
    assert Scope.SINGLETON == "singleton"
    assert Scope.PROTOTYPE == "prototype"


class TestBeanDefinition:
    def test_bean_definition_initialization(self):
        """Test BeanDefinition initialization with and without constructor args"""

        class TestClass:
            pass

        # Test without constructor args
        bean_def = BeanDefinition(TestClass, Scope.SINGLETON)
        assert bean_def.implementation_class == TestClass
        assert bean_def.scope == Scope.SINGLETON
        assert bean_def.constructor_args == {}

        # Test with constructor args
        constructor_args = {"arg1": "value1", "arg2": "value2"}
        bean_def = BeanDefinition(TestClass, Scope.PROTOTYPE, constructor_args)
        assert bean_def.implementation_class == TestClass
        assert bean_def.scope == Scope.PROTOTYPE
        assert bean_def.constructor_args == constructor_args


class TestDependencyConfiguration:
    def setup_method(self):
        """Reset the singleton instance before each test"""
        DependencyConfiguration._instance = None
        self.config = DependencyConfiguration.get_instance()

    def test_singleton_instance(self):
        """Test that DependencyConfiguration maintains singleton pattern"""
        config1 = DependencyConfiguration.get_instance()
        config2 = DependencyConfiguration.get_instance()
        assert config1 is config2

    def test_initial_state(self):
        """Test initial state of DependencyConfiguration"""
        assert "default" in self.config.profiles
        assert self.config.active_profiles == ["default"]

    def test_set_active_profiles(self):
        """Test setting active profiles"""
        self.config.set_active_profiles(["dev", "test"])
        assert self.config.active_profiles == ["default", "dev", "test"]

        # Test with default in middle - should move to front
        self.config.set_active_profiles(["dev", "default", "test"])
        assert self.config.active_profiles == ["default", "dev", "test"]

    def test_get_active_profiles(self):
        """Test getting active profiles returns a copy"""
        profiles = self.config.get_active_profiles()
        profiles.append("new_profile")
        assert "new_profile" not in self.config.active_profiles

    def test_register_bean(self):
        """Test registering beans with different configurations"""

        class TestInterface:
            pass

        class TestImplementation(TestInterface):
            pass

        # Test registering bean in default profile
        self.config.register_bean(TestInterface, TestImplementation, Scope.SINGLETON)

        assert (
            TestInterface.__name__ in self.config.profiles["default"].bean_definitions
        )
        bean_def = self.config.profiles["default"].bean_definitions[
            TestInterface.__name__
        ]
        assert bean_def.implementation_class == TestImplementation
        assert bean_def.scope == Scope.SINGLETON

        # Test registering bean in custom profile
        self.config.register_bean(
            TestInterface,
            TestImplementation,
            Scope.PROTOTYPE,
            {"param": "value"},
            "dev",
        )

        assert "dev" in self.config.profiles
        assert TestInterface.__name__ in self.config.profiles["dev"].bean_definitions
        bean_def = self.config.profiles["dev"].bean_definitions[TestInterface.__name__]
        assert bean_def.implementation_class == TestImplementation
        assert bean_def.scope == Scope.PROTOTYPE
        assert bean_def.constructor_args == {"param": "value"}
