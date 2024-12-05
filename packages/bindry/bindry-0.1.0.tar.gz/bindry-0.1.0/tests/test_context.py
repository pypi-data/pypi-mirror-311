import os
import tempfile
from typing import List, Optional

import pytest
import yaml

from bindry.config import DependencyConfiguration
from bindry.context import ApplicationContext
from bindry.exceptions import DependencyInjectionException
from bindry.scope import Scope


class TestApplicationContext:
    def setup_method(self):
        """Reset singleton instances before each test"""
        self.temp_dir = tempfile.mkdtemp()
        ApplicationContext._instance = None
        DependencyConfiguration._instance = None
        self.context = ApplicationContext.get_instance()
        self.config = DependencyConfiguration.get_instance()

    def teardown_method(self):
        """Cleanup after tests"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def create_config_file(self, filename, content):
        """Helper to create configuration files"""
        path = os.path.join(self.temp_dir, filename)
        with open(path, "w") as f:
            yaml.dump(content, f)
        return path

    def test_singleton_instance(self):
        """Test ApplicationContext maintains singleton pattern"""
        context1 = ApplicationContext.get_instance()
        context2 = ApplicationContext.get_instance()
        assert context1 is context2
        assert hasattr(context1, "ioc_compoment_instances")

    def test_bean_lifecycle_singleton(self):
        """Test singleton bean lifecycle"""

        class TestService:
            def __init__(self):
                self.counter = 0

        self.config.register_bean(TestService, TestService, Scope.SINGLETON)

        # Get the same instance twice
        instance1 = self.context.get_bean(TestService)
        instance1.counter = 1
        instance2 = self.context.get_bean(TestService)

        assert instance1 is instance2
        assert instance2.counter == 1

    def test_bean_lifecycle_prototype(self):
        """Test prototype bean lifecycle"""

        class TestService:
            def __init__(self):
                self.counter = 0

        self.config.register_bean(TestService, TestService, Scope.PROTOTYPE)

        # Get different instances
        instance1 = self.context.get_bean(TestService)
        instance1.counter = 1
        instance2 = self.context.get_bean(TestService)

        assert instance1 is not instance2
        assert instance2.counter == 0

    def test_complex_dependency_injection(self):
        """Test complex dependency injection with multiple levels"""

        class IDatabase:
            pass

        class ICache:
            pass

        class IService:
            pass

        class Database(IDatabase):
            def __init__(self, url: str = "default"):
                self.url = url

        class Cache(ICache):
            def __init__(self, timeout: int = 300):
                self.timeout = timeout

        class Service(IService):
            def __init__(self, db: IDatabase, cache: ICache):
                self.db = db
                self.cache = cache

        # Register components
        self.config.register_bean(
            IDatabase, Database, Scope.SINGLETON, {"url": "mysql://localhost"}
        )
        self.config.register_bean(ICache, Cache, Scope.SINGLETON, {"timeout": 600})
        self.config.register_bean(IService, Service, Scope.SINGLETON)

        # Get service instance
        service = self.context.get_bean(IService)

        assert isinstance(service.db, Database)
        assert isinstance(service.cache, Cache)
        assert service.db.url == "mysql://localhost"
        assert service.cache.timeout == 600

    def test_profile_based_injection(self):
        """Test dependency injection with different profiles"""

        class IMessageService:
            def get_prefix(self) -> str:
                pass

        class DevMessageService(IMessageService):
            def get_prefix(self) -> str:
                return "DEV"

        class ProdMessageService(IMessageService):
            def get_prefix(self) -> str:
                return "PROD"

        # Register implementations in different profiles
        self.config.register_bean(
            IMessageService, DevMessageService, Scope.SINGLETON, profile="dev"
        )
        self.config.register_bean(
            IMessageService, ProdMessageService, Scope.SINGLETON, profile="prod"
        )

        # Test dev profile
        self.config.set_active_profiles(["dev"])
        dev_service = self.context.get_bean(IMessageService)
        assert isinstance(dev_service, DevMessageService)
        assert dev_service.get_prefix() == "DEV"

        # Reset context for prod profile
        ApplicationContext._instance = None
        self.context = ApplicationContext.get_instance()
        self.config.set_active_profiles(["prod"])
        prod_service = self.context.get_bean(IMessageService)
        assert isinstance(prod_service, ProdMessageService)
        assert prod_service.get_prefix() == "PROD"

    def test_autowired_constructor_injection(self):
        """Test constructor injection with optional and required dependencies"""

        class IDependency:
            pass

        class Dependency(IDependency):
            pass

        class ServiceWithRequired:
            def __init__(self, dep: IDependency):
                self.dep = dep

        # Register components
        self.config.register_bean(IDependency, Dependency, Scope.SINGLETON)
        self.config.register_bean(
            ServiceWithRequired, ServiceWithRequired, Scope.SINGLETON
        )

        # Test required injection
        service_req = self.context.get_bean(ServiceWithRequired)
        assert isinstance(service_req.dep, Dependency)

    def test_error_handling(self):
        """Test error handling in bean creation and injection"""

        class UnregisteredDependency:
            pass

        class BrokenService:
            def __init__(self, dep: UnregisteredDependency):
                self.dep = dep

        # Test unregistered dependency
        self.config.register_bean(BrokenService, BrokenService, Scope.SINGLETON)
        with pytest.raises(DependencyInjectionException) as exc_info:
            self.context.get_bean(BrokenService)
        assert "not found in any active profile" in str(exc_info.value)

    def test_varargs_kwargs_handling(self):
        """Test handling of *args and **kwargs in constructors"""

        class ServiceWithVarargs:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        # Register with constructor args
        constructor_args = {"args": [1, 2, 3], "kwargs": {"name": "test", "value": 42}}
        self.config.register_bean(
            ServiceWithVarargs, ServiceWithVarargs, Scope.SINGLETON, constructor_args
        )

        # Get instance and verify args/kwargs
        service = self.context.get_bean(ServiceWithVarargs)
        assert service.args == (1, 2, 3)
        assert service.kwargs == {"name": "test", "value": 42}

    def test_load_configuration(self):
        """Test loading full configuration from file"""

        # Define test classes inside the test function
        class IDatabase:
            pass

        class DevDatabase(IDatabase):
            def __init__(self, host, port):
                self.host = host
                self.port = port

        # Create configuration content using the fully qualified class names
        # from the current module
        module_name = f"{self.__class__.__module__}"
        config_content = {
            "profiles": {
                "dev": {
                    "beans": {
                        "IDatabase": {  # Changed to match class name
                            "bean_type": f"{module_name}.IDatabase",
                            "implementation": f"{module_name}.DevDatabase",
                            "scope": "singleton",
                            "constructor_args": {
                                "host": "${DB_HOST:localhost}",
                                "port": "${DB_PORT:5432}",
                            },
                        }
                    }
                }
            }
        }

        # Create config file
        config_file = self.create_config_file("config.yaml", config_content)

        # Set test classes in the module's namespace
        import sys

        current_module = sys.modules[self.__class__.__module__]
        setattr(current_module, "IDatabase", IDatabase)
        setattr(current_module, "DevDatabase", DevDatabase)

        # Load configuration
        self.context.load_configuration(config_file, active_profiles=["dev"])

        # Verify configuration was loaded
        profiles = self.config.profiles
        assert "dev" in profiles
        assert "IDatabase" in profiles["dev"].bean_definitions

        # Verify bean definition
        bean_def = profiles["dev"].bean_definitions["IDatabase"]
        assert bean_def.implementation_class == DevDatabase
        assert bean_def.scope == "singleton"
        assert bean_def.constructor_args["host"] == "localhost"
        assert bean_def.constructor_args["port"] == "5432"

    def test_set_active_profiles_ordering(self):
        """Test that set_active_profiles maintains correct profile order with default profile"""
        # Test adding profiles without default
        self.context.set_active_profiles(["dev", "test"])
        assert self.config.active_profiles == ["default", "dev", "test"]

        # Test adding profiles with default already included
        self.context.set_active_profiles(["default", "prod", "staging"])
        assert self.config.active_profiles == ["default", "prod", "staging"]

        # Test empty profile list
        self.context.set_active_profiles([])
        assert self.config.active_profiles == ["default"]

    def test_get_bean_profile_override(self):
        """Test that later profiles override earlier ones for bean definitions"""

        class TestInterface:
            pass

        class DevImpl(TestInterface):
            pass

        class ProdImpl(TestInterface):
            pass

        # Register same interface in multiple profiles
        self.config.register_bean(
            TestInterface, DevImpl, Scope.SINGLETON, profile="dev"
        )
        self.config.register_bean(
            TestInterface, ProdImpl, Scope.SINGLETON, profile="prod"
        )

        # Test dev profile first
        self.context.set_active_profiles(["dev", "prod"])
        instance = self.context.get_bean(TestInterface)
        assert isinstance(instance, ProdImpl)  # prod should override dev

        # Test prod profile first
        self.context.set_active_profiles(["prod", "dev"])
        instance = self.context.get_bean(TestInterface)
        assert isinstance(instance, DevImpl)  # dev should override prod

    def test_get_bean_constructor_args_handling(self):
        """Test different types of constructor arguments"""

        class ComplexService:
            def __init__(self, required_arg, *args, optional_arg="default", **kwargs):
                self.required_arg = required_arg
                self.args = args
                self.optional_arg = optional_arg
                self.kwargs = kwargs

        # Test with various constructor argument combinations
        constructor_args = {
            "required_arg": "test",
            "args": [1, 2, 3],
            "optional_arg": "custom",
            "kwargs": {"extra1": "value1", "extra2": "value2"},
        }

        self.config.register_bean(
            ComplexService, ComplexService, Scope.SINGLETON, constructor_args
        )

        instance = self.context.get_bean(ComplexService)
        assert instance.required_arg == "test"
        assert instance.args == (1, 2, 3)
        assert instance.optional_arg == "custom"
        assert instance.kwargs == {"extra1": "value1", "extra2": "value2"}

    def test_get_bean_dependency_chain(self):
        """Test nested dependency injection with multiple levels"""

        class Level3:
            def __init__(self, value="level3"):
                self.value = value

        class Level2:
            def __init__(self, level3: Level3, extra="level2"):
                self.level3 = level3
                self.extra = extra

        class Level1:
            def __init__(self, level2: Level2):
                self.level2 = level2

        # Register beans with dependencies
        self.config.register_bean(Level3, Level3, Scope.SINGLETON)
        self.config.register_bean(Level2, Level2, Scope.SINGLETON)
        self.config.register_bean(Level1, Level1, Scope.SINGLETON)

        # Get top-level bean
        instance = self.context.get_bean(Level1)

        # Verify entire dependency chain
        assert isinstance(instance, Level1)
        assert isinstance(instance.level2, Level2)
        assert isinstance(instance.level2.level3, Level3)
        assert instance.level2.level3.value == "level3"
        assert instance.level2.extra == "level2"

    def test_get_bean_error_cases(self):
        """Test error handling in get_bean"""

        class UnregisteredService:
            pass

        class BrokenService:
            def __init__(self, missing_dependency: UnregisteredService):
                self.dep = missing_dependency

        # Test unregistered bean
        with pytest.raises(DependencyInjectionException) as exc_info:
            self.context.get_bean(UnregisteredService)
        assert "not found in any active profile" in str(exc_info.value)

        # Test missing dependency
        self.config.register_bean(BrokenService, BrokenService, Scope.SINGLETON)
        with pytest.raises(DependencyInjectionException) as exc_info:
            self.context.get_bean(BrokenService)
        assert "not found in any active profile" in str(exc_info.value)

    def test_get_bean_keyword_only_args(self):
        """Test handling of keyword-only arguments"""

        class ServiceWithKeywordOnly:
            def __init__(self, *, required_kw, optional_kw="default"):
                self.required_kw = required_kw
                self.optional_kw = optional_kw

        # Register with keyword-only args
        constructor_args = {"required_kw": "test", "optional_kw": "custom"}
        self.config.register_bean(
            ServiceWithKeywordOnly,
            ServiceWithKeywordOnly,
            Scope.SINGLETON,
            constructor_args,
        )

        instance = self.context.get_bean(ServiceWithKeywordOnly)
        assert instance.required_kw == "test"
        assert instance.optional_kw == "custom"

    def test_get_bean_scope_behavior(self):
        """Test bean scoping behavior with complex dependencies"""

        class SingletonDep:
            def __init__(self):
                self.id = id(self)

        class PrototypeDep:
            def __init__(self):
                self.id = id(self)

        class MixedService:
            def __init__(self, singleton: SingletonDep, prototype: PrototypeDep):
                self.singleton = singleton
                self.prototype = prototype

        # Register dependencies with different scopes
        self.config.register_bean(SingletonDep, SingletonDep, Scope.SINGLETON)
        self.config.register_bean(PrototypeDep, PrototypeDep, Scope.PROTOTYPE)
        self.config.register_bean(MixedService, MixedService, Scope.PROTOTYPE)

        # Get service instances
        instance1 = self.context.get_bean(MixedService)
        instance2 = self.context.get_bean(MixedService)

        # Verify scoping behavior
        assert instance1 is not instance2  # Prototype scope
        assert instance1.singleton is instance2.singleton  # Singleton dependency
        assert instance1.prototype is not instance2.prototype  # Prototype dependency

    def test_get_bean_constructor_failures(self):
        """Test different constructor failure scenarios and error handling"""

        # Test case 1: Class with __init__ that raises AttributeError
        class BrokenConstructor:
            def __init__(self):
                raise AttributeError("Simulated broken constructor")

        self.config.register_bean(BrokenConstructor, BrokenConstructor, Scope.SINGLETON)

        # Should handle AttributeError and create instance
        with pytest.raises(AttributeError, match="Simulated broken constructor"):
            self.context.get_bean(BrokenConstructor)

        # Test case 2: Class that fails with TypeError on full constructor args
        class PickyConstructor:
            def __init__(self, *args, **kwargs):
                if args or kwargs:  # Fails if any arguments are provided
                    raise TypeError("Don't want any arguments!")
                self.initialized = True

        self.config.register_bean(
            PickyConstructor,
            PickyConstructor,
            Scope.SINGLETON,
            constructor_args={"args": [1, 2], "kwargs": {"a": "b"}},
        )

        # Should fall back to kwargs-only instantiation
        with pytest.raises(TypeError, match="Don't want any arguments!"):
            self.context.get_bean(PickyConstructor)

    def test_get_bean_parameter_handling(self):
        """Test various parameter handling scenarios including keyword-only parameters"""

        # Test case 1: Class with mix of parameter types
        class ComplexParams:
            def __init__(self, pos_only, /, normal, *, kw_only):
                self.pos_only = pos_only
                self.normal = normal
                self.kw_only = kw_only

        constructor_args = {"pos_only": "pos", "normal": "norm", "kw_only": "kw"}

        self.config.register_bean(
            ComplexParams, ComplexParams, Scope.SINGLETON, constructor_args
        )

        instance = self.context.get_bean(ComplexParams)
        assert instance.pos_only == "pos"
        assert instance.normal == "norm"
        assert instance.kw_only == "kw"

    def test_get_bean_dependency_resolution_failure(self):
        """Test scenarios where dependency resolution fails"""

        # Test case 1: Missing required parameter with no default
        class RequiredDep:
            def __init__(self, required_param):
                self.required_param = required_param

        self.config.register_bean(RequiredDep, RequiredDep, Scope.SINGLETON)

        with pytest.raises(DependencyInjectionException) as exc_info:
            self.context.get_bean(RequiredDep)
        assert "Cannot resolve parameter" in str(exc_info.value)

    def test_get_bean_complex_kwargs_handling(self):
        """Test complex kwargs handling scenarios"""

        class KwargsHandler:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        # Test case 1: Constructor args with special keys
        constructor_args = {"args": [1, 2], "kwargs": {"a": 1}, "extra_kwarg": "value"}

        self.config.register_bean(
            KwargsHandler, KwargsHandler, Scope.SINGLETON, constructor_args
        )

        instance = self.context.get_bean(KwargsHandler)
        assert instance.kwargs.get("a") == 1
        assert instance.kwargs.get("extra_kwarg") == "value"
        assert "args" not in instance.kwargs  # Special key should be handled separately
