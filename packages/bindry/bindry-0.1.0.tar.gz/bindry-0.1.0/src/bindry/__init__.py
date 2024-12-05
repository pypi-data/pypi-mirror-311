"""
Bindry: Elegant Python Dependency Injection with Profile-Aware Configuration
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bindry")
except PackageNotFoundError:
    __version__ = "unknown"

# Configuration
from .config import BeanDefinition, DependencyConfiguration, ProfileConfig
from .context import ApplicationContext

# Decorators
from .decorators import autowired, component
from .exceptions import DependencyInjectionException
from .loader import ConfigurationLoader

# Core components
from .scope import Scope

# Utils
from .utils import locate

__all__ = [
    # Version
    "__version__",
    # Core
    "Scope",
    "DependencyInjectionException",
    "ApplicationContext",
    # Decorators
    "component",
    "autowired",
    # Configuration
    "DependencyConfiguration",
    "BeanDefinition",
    "ProfileConfig",
    # Utils
    "locate",
    "ConfigurationLoader",
]
