import pytest

from bindry.config import DependencyConfiguration
from bindry.context import ApplicationContext
from bindry.decorators import autowired, component
from bindry.exceptions import DependencyInjectionException
from bindry.scope import Scope


class TestComponentDecorator:
    def setup_method(self):
        """Reset the dependency configuration before each test"""
        DependencyConfiguration._instance = None
        ApplicationContext._instance = None
        self.config = DependencyConfiguration.get_instance()

    def test_basic_component_registration(self):
        """Test basic component registration without bean type"""

        @component(Scope.SINGLETON)
        class TestService:
            pass

        assert TestService.__name__ in self.config.profiles["default"].bean_definitions
        bean_def = self.config.profiles["default"].bean_definitions[
            TestService.__name__
        ]
        assert bean_def.implementation_class == TestService
        assert bean_def.scope == Scope.SINGLETON

    def test_component_with_interface(self):
        """Test component registration with explicit interface"""

        class ITestService:
            pass

        @component(Scope.SINGLETON, bean_type=ITestService)
        class TestServiceImpl(ITestService):
            pass

        assert ITestService.__name__ in self.config.profiles["default"].bean_definitions
        bean_def = self.config.profiles["default"].bean_definitions[
            ITestService.__name__
        ]
        assert bean_def.implementation_class == TestServiceImpl

    def test_component_with_constructor_args(self):
        """Test component registration with constructor arguments"""

        @component(
            scope=Scope.SINGLETON, constructor_args={"timeout": 30, "retries": 3}
        )
        class ConfigurableService:
            def __init__(self, timeout, retries):
                self.timeout = timeout
                self.retries = retries

        bean_def = self.config.profiles["default"].bean_definitions[
            ConfigurableService.__name__
        ]
        assert bean_def.constructor_args == {"timeout": 30, "retries": 3}

    def test_multi_profile_component(self):
        """Test component registration across multiple profiles"""

        @component(Scope.SINGLETON, profile=["dev", "prod"])
        class MultiProfileService:
            pass

        assert (
            MultiProfileService.__name__ in self.config.profiles["dev"].bean_definitions
        )
        assert (
            MultiProfileService.__name__
            in self.config.profiles["prod"].bean_definitions
        )


class TestAutowiredDecorator:
    def setup_method(self):
        """Reset both configuration and context before each test"""
        DependencyConfiguration._instance = None
        ApplicationContext._instance = None
        self.config = DependencyConfiguration.get_instance()
        self.context = ApplicationContext.get_instance()

    def test_autowired_method_injection(self):
        """Test autowired method injection with dependencies"""

        class IDependency:
            def get_value(self):
                return "test_value"

        # Create implementation
        @component(Scope.SINGLETON, bean_type=IDependency)
        class DependencyImpl(IDependency):
            pass

        # Create service that uses the dependency
        @component(Scope.SINGLETON)
        class TestService:
            def __init__(self):
                self.dependency = None

            @autowired
            def initialize(self, dependency: IDependency):
                self.dependency = dependency
                return self.dependency.get_value()

        # Get the service from context and verify injection
        service = self.context.get_bean(TestService)
        value = service.initialize(_ioc_application_context_=self.context)

        assert service.dependency is not None
        assert isinstance(service.dependency, DependencyImpl)
        assert value == "test_value"

    def test_autowired_missing_annotation(self):
        """Test autowired method with missing type annotation"""

        class TestService:
            @autowired
            def initialize(self, dependency):  # Missing type annotation
                pass

        with pytest.raises(DependencyInjectionException) as exc_info:
            TestService().initialize(_ioc_application_context_=self.context)
        assert "must have a type annotation" in str(exc_info.value)

    def test_autowired_multiple_dependencies(self):
        """Test autowired method with multiple dependencies"""

        class IService1:
            def method1(self):
                return "service1"

        class IService2:
            def method2(self):
                return "service2"

        @component(Scope.SINGLETON, bean_type=IService1)
        class Service1Impl(IService1):
            pass

        @component(Scope.SINGLETON, bean_type=IService2)
        class Service2Impl(IService2):
            pass

        @component(Scope.SINGLETON)
        class TestService:
            def __init__(self):
                self.service1 = None
                self.service2 = None

            @autowired
            def initialize(self, service1: IService1, service2: IService2):
                self.service1 = service1
                self.service2 = service2
                return (self.service1.method1(), self.service2.method2())

        # Get the service and test injection
        service = self.context.get_bean(TestService)
        result1, result2 = service.initialize(_ioc_application_context_=self.context)

        assert isinstance(service.service1, Service1Impl)
        assert isinstance(service.service2, Service2Impl)
        assert result1 == "service1"
        assert result2 == "service2"

    def test_prototype_scope_injection(self):
        """Test autowired injection with prototype scope"""

        class IPrototype:
            pass

        @component(Scope.PROTOTYPE, bean_type=IPrototype)
        class PrototypeImpl(IPrototype):
            def __init__(self):
                self.id = id(self)

        @component(Scope.SINGLETON)
        class TestService:
            def __init__(self):
                self.dep1 = None
                self.dep2 = None

            @autowired
            def initialize(self, dep1: IPrototype, dep2: IPrototype):
                self.dep1 = dep1
                self.dep2 = dep2

        # Get the service and inject dependencies
        service = self.context.get_bean(TestService)
        service.initialize(_ioc_application_context_=self.context)

        # Verify that prototype scope creates different instances
        assert isinstance(service.dep1, PrototypeImpl)
        assert isinstance(service.dep2, PrototypeImpl)
        assert service.dep1 is not service.dep2
        assert service.dep1.id != service.dep2.id
