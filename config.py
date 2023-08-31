import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
SECRETS_PATH = os.path.join(os.path.dirname(__file__), "secrets.yaml")


class Config:
    CONFIG = dict()
    with open(CONFIG_PATH) as config_file:
        CONFIG = yaml.safe_load(config_file)

    with open(SECRETS_PATH) as secrets_file:
        CONFIG["Secrets"] = yaml.safe_load(secrets_file)
