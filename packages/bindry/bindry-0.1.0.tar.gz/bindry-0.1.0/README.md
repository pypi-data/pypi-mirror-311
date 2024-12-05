# Bindry

Elegant Python Dependency Injection with Profile-Aware Configuration

[![PyPI version](https://badge.fury.io/py/bindry.svg)](https://badge.fury.io/py/bindry)
[![Python Support](https://img.shields.io/pypi/pyversions/bindry.svg)](https://pypi.org/project/bindry/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Bindry is a powerful yet intuitive dependency injection framework for Python that supports profile-based configuration, environment variable interpolation, and flexible component lifecycle management. It enables you to write more maintainable and testable applications by managing dependencies through configuration rather than hard-coding them.

## Features

- Profile-based configuration management
- Environment variable support with fallback values
- YAML and JSON configuration file support
- Constructor, method, and property injection
- Singleton and prototype scoping
- Type-based automatic dependency resolution
- Support for constructor arguments via configuration
- Flexible component registration through decorators or configuration files

## Installation

```bash
pip install bindry
```

## Quick Start

### 1. Define Your Components

```python
from bindry import component, Scope, autowired

# Define an interface
class MessageService:
    def send_message(self, msg: str): pass

# Implement the service
@component(scope=Scope.SINGLETON, bean_type=MessageService)
class EmailService(MessageService):
    def send_message(self, msg: str):
        print(f"Sending email: {msg}")

# Use dependency injection
@component(scope=Scope.SINGLETON)
class NotificationManager:
    @autowired
    def __init__(self, message_service: MessageService):
        self.message_service = message_service

    def notify(self, message: str):
        self.message_service.send_message(message)
```

### 2. Configure Your Application

Create a `config.yaml` file:

```yaml
profiles:
  default:
    beans:
      MessageService:
        bean_type: "myapp.services.MessageService"
        implementation: "myapp.services.EmailService"
        scope: "singleton"
        constructor_args:
          timeout: 30

  development:
    beans:
      MessageService:
        bean_type: "myapp.services.MessageService"
        implementation: "myapp.services.MockMessageService"
        scope: "prototype"
```

### 3. Initialize and Use

```python
from bindry import ApplicationContext

# Initialize the context
context = ApplicationContext.get_instance()
context.load_configuration("config.yaml", active_profiles=["development"])

# Get and use components
notification_manager = context.get_bean(NotificationManager)
notification_manager.notify("Hello, World!")
```

## Environment Variable Support

Bindry supports environment variable interpolation in configuration files:

```yaml
profiles:
  default:
    beans:
      DatabaseService:
        constructor_args:
          url: "${DATABASE_URL:sqlite:///default.db}"
          timeout: "${DB_TIMEOUT:30}"
```

## Profile Management

### Using Multiple Profiles

```python
context = ApplicationContext.get_instance()
context.set_active_profiles(["default", "development", "testing"])
```

### Environment-Based Profiles

Set the `ACTIVE_PROFILES` environment variable:

```bash
export ACTIVE_PROFILES=development,testing
```

## Advanced Features

### Constructor Argument Injection

```python
@component(
    scope=Scope.SINGLETON,
    constructor_args={
        "timeout": 30,
        "retries": 3,
        "kwargs": {"debug": True}
    }
)
class DatabaseService:
    def __init__(self, timeout: int, retries: int, **kwargs):
        self.timeout = timeout
        self.retries = retries
        self.debug = kwargs.get("debug", False)
```

### Method Injection

```python
@component(Scope.SINGLETON)
class ServiceManager:
    @autowired
    def configure(self, config_service: ConfigService):
        self.config_service = config_service
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was developed with the assistance of AI language models:
- Initial implementation assistance provided by ChatGPT
- Additional feature development and refinements by Claude.ai

While the code was primarily generated through AI assistance, all implementations have been carefully reviewed and tested to ensure quality and reliability.