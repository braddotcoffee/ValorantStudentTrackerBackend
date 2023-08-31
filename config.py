import yaml
import os

class YAMLConfig:
    CONFIG = dict()
    with open(
        os.path.join(os.path.dirname(__file__), "config.yaml")
    ) as config_file:
        CONFIG = yaml.safe_load(config_file)

    secrets_path = os.path.join(os.path.dirname(__file__), "secrets.yaml")
    if os.path.exists(secrets_path):
        with open(secrets_path) as secrets_file:
            CONFIG["Secrets"] = yaml.safe_load(secrets_file)
    else:
        CONFIG["Secrets"] = {"Google": {"API_KEY": os.environ["GOOGLE_API_KEY"]}}