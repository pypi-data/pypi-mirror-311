import sys

import pytest

from bindry.exceptions import DependencyInjectionException
from bindry.utils import locate


class TestLocate:
    """Test suite for the locate utility function"""

    def setup_method(self):
        """Setup before each test"""
        self.current_module = sys.modules[self.__class__.__module__]
        self.cleanup_attrs = []

    def teardown_method(self):
        """Cleanup after each test"""
        for attr in self.cleanup_attrs:
            if hasattr(self.current_module, attr):
                delattr(self.current_module, attr)

    def test_valid_class_location(self):
        """Test locating a valid class from a module"""

        class TestClass:
            pass

        # Add the class to the module namespace
        setattr(self.current_module, "TestClass", TestClass)
        self.cleanup_attrs.append("TestClass")

        # Get the full path and test
        class_path = f"{self.current_module.__name__}.TestClass"
        located_class = locate(class_path)
        assert located_class is TestClass

    def test_builtin_class_location(self):
        """Test locating built-in Python classes"""
        # For built-in types, we need to use their full path
        assert locate("builtins.str") is str
        assert locate("builtins.dict") is dict
        assert locate("builtins.list") is list

    def test_builtin_direct_location(self):
        """Test locating built-in Python classes without module path"""
        assert locate("str") is str
        assert locate("dict") is dict
        assert locate("list") is list
        assert locate("int") is int
        assert locate("float") is float
        assert locate("bool") is bool
        assert locate("tuple") is tuple
        assert locate("set") is set

    def test_invalid_class_path(self):
        """Test error handling for invalid class paths"""
        with pytest.raises(DependencyInjectionException):
            locate(None)
        with pytest.raises(DependencyInjectionException):
            locate("")
        with pytest.raises(DependencyInjectionException):
            locate(123)

    def test_nonexistent_module(self):
        """Test error handling for non-existent modules"""
        with pytest.raises(ImportError):
            locate("nonexistent_module.NonexistentClass")

    def test_nonexistent_class(self):
        """Test error handling for non-existent classes in valid modules"""
        with pytest.raises(ImportError):
            locate("os.NonexistentClass")

    def test_invalid_format(self):
        """Test error handling for improperly formatted class paths"""
        with pytest.raises(DependencyInjectionException) as exc_info:
            locate("invalid..path")
        assert "Invalid class path format" in str(exc_info.value)

        with pytest.raises(DependencyInjectionException) as exc_info:
            locate(".invalid.path")
        assert "Invalid class path format" in str(exc_info.value)

        with pytest.raises(DependencyInjectionException) as exc_info:
            locate("invalid.path.")
        assert "Invalid class path format" in str(exc_info.value)

    def test_nested_class_location(self):
        """Test locating nested classes"""

        class OuterClass:
            class InnerClass:
                pass

        # Add the outer class to the module namespace
        module_name = self.current_module.__name__
        setattr(self.current_module, "OuterClass", OuterClass)
        self.cleanup_attrs.append("OuterClass")

        # For nested classes, we'll get the outer class first
        outer = locate(f"{module_name}.OuterClass")
        assert outer is OuterClass
        # Then access the inner class as an attribute
        assert outer.InnerClass is OuterClass.InnerClass

    def test_module_level_function(self):
        """Test locating module-level functions"""

        def test_function():
            pass

        # Add function to module namespace
        setattr(self.current_module, "test_function", test_function)
        self.cleanup_attrs.append("test_function")

        function_path = f"{self.current_module.__name__}.test_function"
        located_function = locate(function_path)
        assert located_function is test_function

    def test_complex_path_handling(self):
        """Test handling of complex import paths"""

        class Level1:
            class Level2:
                class Level3:
                    pass

        # Add the top-level class to the module namespace
        module_name = self.current_module.__name__
        setattr(self.current_module, "Level1", Level1)
        self.cleanup_attrs.append("Level1")

        # Navigate the nested structure one level at a time
        level1 = locate(f"{module_name}.Level1")
        assert level1 is Level1
        assert level1.Level2 is Level1.Level2
        assert level1.Level2.Level3 is Level1.Level2.Level3

    def test_module_attributes(self):
        """Test locating module attributes"""
        import math

        assert locate("math.pi") == math.pi
        assert locate("math.e") == math.e
