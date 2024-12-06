import os
from dotenv import load_dotenv, find_dotenv


def _set_env_vars():
    """
    Internal function to load environment variables based on the environment type.
    """
    is_dev_env = os.getenv("FLASK_DEV_ENV")
    env_file_name = ".env.dev" if is_dev_env else ".env.prod"

    env_file = find_dotenv(env_file_name)
    if env_file:
        load_dotenv(env_file, override=False)
    else:
        raise FileNotFoundError(
            f"Environment file not found: {env_file_name}. Searched in the project root."
        )


def _validate_env_vars():
    """
    Internal function to validate that all required environment variables are set.
    """
    example_file = find_dotenv(".env.example")
    if not example_file:
        raise FileNotFoundError(
            "The '.env.example' file is missing in the project root. "
            "This file is required to validate environment variables."
        )

    required_keys = []
    with open(example_file, "r") as file:
        for line in file:
            # Ignoring comments and blank lines
            line = line.strip()
            if line and not line.startswith("#"):
                key = line.split("=")[0].strip()
                required_keys.append(key)

    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise ValueError(
            f"The following required environment variables are missing: {', '.join(missing_keys)}"
        )


def initialize_env():
    """
    Public function to initialize and validate environment variables.
    Call this function at the start of your project.
    """
    try:
        _set_env_vars()
        _validate_env_vars()
    except Exception as e:
        raise Exception(f"Error initializing environment variables: {str(e)}")
