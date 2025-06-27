import yaml


def load_config(config_path: str) -> dict:
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError(f"Config file {config_path} is not a valid YAML dictionary.")

        print(f"Configuration from {config_path} loaded successfully.")
        return config

    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error while loading config: {e}")

    return {}