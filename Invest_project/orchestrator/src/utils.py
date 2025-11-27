import yaml
from pathlib import Path
from datetime import datetime, timedelta


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


def update_config(config_path: str, key: str, value, section: str = None):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        if section:
            if section not in config:
                config[section] = {}
            config[section][key] = value
        else:
            config[key] = value

        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

        print(f"Config {config_path} updated successfully: {key} = {value}")

    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error while parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error while updating config: {e}")


def get_start_end_dates(variables: dict, section: str, key: str) -> tuple:
    start_date = variables.get(section, {}).get(key)
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        if start_date >= datetime.today():
            return "", ""
    else:
        start_date = datetime.today()

    end_date = datetime.today() - timedelta(days=1)
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    return start_date, end_date
