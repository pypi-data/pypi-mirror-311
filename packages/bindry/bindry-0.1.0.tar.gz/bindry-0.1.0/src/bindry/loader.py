import json
import os
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv

from .config import DependencyConfiguration
from .exceptions import DependencyInjectionException
from .scope import Scope
from .utils import locate


class ConfigurationLoader:
    """
    Handles the loading and processing of configuration files with support for
    profile-specific settings, .env files, and environment variable interpolation.

    This class provides methods to:
    - Load environment variables from a base `.env` file and profile-specific `.env` files.
    - Process configuration dictionaries to replace placeholders with actual environment variable values.
    """

    @staticmethod
    def load_profile_environment_variables(
        profile: str = "default", base_env_file: str = ".env"
    ) -> None:
        """
        Loads environment variables for a specific profile.

        The method first loads the base `.env` file (if it exists) and then
        loads a profile-specific `.env` file (e.g., `.env.dev`) if the profile is not "default".
        Profile-specific variables override base variables.

        Args:
            profile (str): The profile name (e.g., "dev", "prod"). Defaults to "default".
            base_env_file (str): The name of the base `.env` file. Defaults to ".env".
        """
        # Load base .env first if it exists
        if os.path.exists(base_env_file):
            load_dotenv(base_env_file)

        # If profile is not default, load profile-specific .env
        if profile != "default":
            profile_env_file = f"{base_env_file}.{profile}"
            if os.path.exists(profile_env_file):
                # override=True allows profile-specific vars to override base vars
                load_dotenv(profile_env_file, override=True)
            else:
                print(
                    f"Warning: Profile environment file '{profile_env_file}' not found"
                )

    @staticmethod
    def load_environment_variables(
        active_profiles: List[str], base_env_file: str = ".env"
    ) -> None:
        """
        Loads environment variables for all active profiles in the specified order.

        The method first loads the base `.env` file and then iterates through
        the list of active profiles, loading profile-specific `.env` files for
        each profile in sequence. Variables from later profiles override those
        from earlier ones.

        Args:
            active_profiles (List[str]): List of active profile names, in priority order.
            base_env_file (str): The name of the base `.env` file. Defaults to ".env".
        """
        # First load the default/base environment
        ConfigurationLoader.load_profile_environment_variables("default", base_env_file)

        # Then load each profile's environment variables in order
        for profile in active_profiles:
            if profile != "default":  # Skip default as it's already loaded
                ConfigurationLoader.load_profile_environment_variables(
                    profile, base_env_file
                )

    @staticmethod
    def interpolate_env_vars(value: str) -> str:
        """
        Replaces placeholders in a string with corresponding environment variable values.

        Supports the following formats:
        - `${ENV_VAR}`: Uses the value of the environment variable `ENV_VAR`.
        - `$ENV_VAR`: Equivalent to `${ENV_VAR}`.
        - `${ENV_VAR:default}`: Uses `default` if `ENV_VAR` is not set.

        Args:
            value (str): The input string containing placeholders for environment variables.

        Returns:
            str: The string with placeholders replaced by environment variable values.
        """
        if not isinstance(value, str):
            return value

        import re

        pattern = r"\$\{([^}]+)\}|\$([A-Za-z0-9_]+)"

        def replace_env_var(match):
            env_var = match.group(1) or match.group(2)
            default_value = None

            if ":" in env_var:
                env_var, default_value = env_var.split(":", 1)

            return os.environ.get(
                env_var, default_value if default_value is not None else f"${env_var}"
            )

        return re.sub(pattern, replace_env_var, value)

    @staticmethod
    def process_config_values(config: Dict) -> Dict:
        """
        Recursively processes a configuration dictionary, replacing placeholders
        in strings with corresponding environment variable values.

        For nested dictionaries and lists, the method applies interpolation
        recursively to all string values.

        Args:
            config (Dict): The input configuration dictionary.

        Returns:
            Dict: The processed configuration dictionary with interpolated values.
        """
        processed_config: Dict[str, Any] = {}

        for key, value in config.items():
            if isinstance(value, dict):
                processed_config[key] = ConfigurationLoader.process_config_values(value)
            elif isinstance(value, list):
                processed_config[key] = [
                    (
                        ConfigurationLoader.process_config_values(item)
                        if isinstance(item, dict)
                        else ConfigurationLoader.interpolate_env_vars(item)
                    )
                    for item in value
                ]
            else:
                processed_config[key] = ConfigurationLoader.interpolate_env_vars(value)

        return processed_config

    @classmethod
    def load_configuration(
        cls,
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
        if active_profiles is None:
            active_profiles = ["default"]

        # Add environment-specified profiles
        env_profiles = os.environ.get("ACTIVE_PROFILES", "").strip()
        if env_profiles:
            active_profiles.extend(env_profiles.split(","))

        # Remove duplicates while preserving order, except for 'default'
        filtered_profiles = []
        seen = set()
        for profile in active_profiles:
            if profile != "default" and profile not in seen:
                filtered_profiles.append(profile)
                seen.add(profile)

        # Create final profile list with 'default' at the beginning
        final_profiles = ["default"] + filtered_profiles

        # Load environment variables for all active profiles
        cls.load_environment_variables(final_profiles, base_env_file)

        file_extension = os.path.splitext(file_path)[1].lower()

        with open(file_path, "r") as file:
            if file_extension == ".yaml" or file_extension == ".yml":
                config_data = yaml.safe_load(file)
            elif file_extension == ".json":
                config_data = json.load(file)
            else:
                raise DependencyInjectionException(
                    f"Unsupported file format: {file_extension}"
                )

        # Process environment variables
        config_data = cls.process_config_values(config_data)

        # Create DependencyConfiguration instance
        dependency_configuration = DependencyConfiguration().get_instance()
        dependency_configuration.set_active_profiles(final_profiles)

        # Process each profile
        for profile_name, profile_data in config_data.get("profiles", {}).items():
            beans_config = profile_data.get("beans", {})

            # Register beans for this profile
            for bean_name, bean_config in beans_config.items():
                bean_type = locate(bean_config["bean_type"])
                implementation_class = locate(bean_config["implementation"])
                scope = bean_config.get("scope", Scope.SINGLETON)
                constructor_args = bean_config.get("constructor_args", {})

                dependency_configuration.register_bean(
                    bean_type=bean_type,
                    implementation_class=implementation_class,
                    scope=scope,
                    constructor_args=constructor_args,
                    profile=profile_name,
                )
