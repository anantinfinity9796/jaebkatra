# util.py

import os
import yaml
from pathlib import Path
from logging.config import dictConfig

def read_app_log_config_file(filepath: str) -> dict:
    with open(filepath) as file:
        log_config_data = yaml.safe_load(file)
    return log_config_data

def initialize_logger():
    filepath = Path(__file__).resolve().parent.parent
    log_config_dict = read_app_log_config_file(filepath=filepath/'conf/app_log_config.yaml')

    log_folder_path = log_config_dict['handlers']['app_handler']['filename'].rsplit("/", maxsplit=1)[0]
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    global logger
    logger = dictConfig(log_config_dict)
    return