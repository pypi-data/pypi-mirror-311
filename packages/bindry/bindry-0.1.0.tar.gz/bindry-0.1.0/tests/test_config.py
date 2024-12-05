import os
import tempfile

import pytest
import yaml

from bindry.config import DependencyConfiguration
from bindry.exceptions import DependencyInjectionException
from bindry.loader import ConfigurationLoader


class TestConfigurationLoader:
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        DependencyConfiguration._instance = None
        self.config = DependencyConfiguration.get_instance()

    def teardown_method(self):
        """Cleanup after tests"""
        import shutil

        shutil.rmtree(self.temp_dir)
        # Clean up environment variables
        for var in ["TEST_VAR", "NUMERIC_VAR", "HOST", "PORT", "PASSWORD"]:
            if var in os.environ:
                del os.environ[var]

    def create_env_file(self, filename, content):
        """Helper to create environment files"""
        path = os.path.join(self.temp_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        return path

    def create_config_file(self, filename, content):
        """Helper to create configuration files"""
        path = os.path.join(self.temp_dir, filename)
        with open(path, "w") as f:
            yaml.dump(content, f)
        return path

    def test_load_environment_variables(self):
        """Test loading environment variables from multiple files"""
        # Create base .env
        base_env = self.create_env_file(".env", "BASE_VAR=base_value\nSHARED_VAR=base")

        # Create profile-specific .env files
        dev_env = self.create_env_file(".env.dev", "DEV_VAR=dev_value\nSHARED_VAR=dev")
        prod_env = self.create_env_file(
            ".env.prod", "PROD_VAR=prod_value\nSHARED_VAR=prod"
        )

        # Test loading with multiple profiles
        ConfigurationLoader.load_environment_variables(
            ["dev", "prod"], base_env_file=base_env
        )

        assert os.environ.get("BASE_VAR") == "base_value"
        assert os.environ.get("DEV_VAR") == "dev_value"
        assert os.environ.get("PROD_VAR") == "prod_value"
        # Last profile should win for shared variables
        assert os.environ.get("SHARED_VAR") == "prod"

    def test_interpolate_env_vars(self):
        """Test environment variable interpolation"""
        os.environ["TEST_VAR"] = "test_value"
        os.environ["NUMERIC_VAR"] = "42"

        # Test basic interpolation
        assert ConfigurationLoader.interpolate_env_vars("${TEST_VAR}") == "test_value"

        # Test with default value
        assert (
            ConfigurationLoader.interpolate_env_vars("${MISSING_VAR:default}")
            == "default"
        )

        # Test mixed content
        assert (
            ConfigurationLoader.interpolate_env_vars(
                "Value is ${TEST_VAR} and ${NUMERIC_VAR}"
            )
            == "Value is test_value and 42"
        )

    def test_process_config_values(self):
        """Test processing configuration values with interpolation"""
        os.environ["HOST"] = "localhost"
        os.environ["PORT"] = "5432"
        os.environ["PASSWORD"] = "secret"

        config = {
            "database": {
                "host": "${HOST}",
                "port": "${PORT}",
                "credentials": {"password": "${PASSWORD}", "timeout": "${TIMEOUT:30}"},
            }
        }

        processed = ConfigurationLoader.process_config_values(config)

        assert processed["database"]["host"] == "localhost"
        assert processed["database"]["port"] == "5432"
        assert processed["database"]["credentials"]["password"] == "secret"
        assert processed["database"]["credentials"]["timeout"] == "30"

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
        ConfigurationLoader.load_configuration(config_file, active_profiles=["dev"])

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
