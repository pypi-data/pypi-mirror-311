import importlib
from typing import Type

from .exceptions import DependencyInjectionException


def locate(class_path: str) -> Type:
    """Dynamically import a class from a module path."""
    if not class_path or not isinstance(class_path, str):
        raise DependencyInjectionException(f"Invalid class path: {class_path}")

    try:
        # Check for obviously invalid paths
        if ".." in class_path or class_path.startswith(".") or class_path.endswith("."):
            raise DependencyInjectionException(
                f"Invalid class path format: {class_path}"
            )

        if "." not in class_path:
            # Handle builtin types
            if isinstance(__builtins__, dict):
                return __builtins__.get(class_path)  # Use dictionary access
            else:
                return getattr(
                    __builtins__, class_path
                )  # Use getattr for module access

        parts = class_path.split(".")
        module_path = parts[0]
        current = importlib.import_module(module_path)

        # Handle multi-part paths (including nested classes)
        for part in parts[1:]:
            current = getattr(current, part)

        return current
    except ImportError as e:
        raise ImportError(f"Could not locate class '{class_path}': {str(e)}")
    except AttributeError as e:
        raise ImportError(f"Could not locate class '{class_path}': {str(e)}")
    except Exception as e:
        raise DependencyInjectionException(
            f"Invalid class path format '{class_path}': {str(e)}"
        )
