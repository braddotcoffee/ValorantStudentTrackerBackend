import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_from_yaml():
    config = None
    with open(CONFIG_PATH) as config_file:
        config = yaml.safe_load(config_file)

    with open(
        os.path.join(os.path.dirname(__file__), "secrets.yaml")
    ) as secrets_file:
        config["Secrets"] = yaml.safe_load(secrets_file)
    return config

def load_from_env():
    return {
        "Google": {
            "SheetID": os.environ["GOOGLE_SHEET_ID"]
        },
        "Secrets": {
            "Google": {
                "API_KEY": os.environ["GOOGLE_API_KEY"]
            }
        }
    }

class Config:
    CONFIG = dict()

    if os.path.exists(CONFIG_PATH):
        CONFIG = load_from_yaml()
    else:
        CONFIG = load_from_env()
