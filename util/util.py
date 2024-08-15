# util.py

import yaml

def read_app_log_config_file(filepath: str) -> dict:
    with open(filepath) as file:
        log_config_data = yaml.safe_load(file)
    return log_config_data