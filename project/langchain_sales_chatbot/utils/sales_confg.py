import json

import yaml


class SalesConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SalesConfig, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def initialize(self, args):
        with open(args.config_file, "r") as f:
            config = yaml.safe_load(f)

        with open("utils/role_info.json", "r") as f:
            role_info = json.loads(f.read())

        # Use the argparse Namespace to update the configuration
        overridden_values = {
            key: value for key, value in vars(args).items() if key in config and value is not None
        }
        config.update(overridden_values)
        enable_chat = config.get("enable_chat")
        config["enable_chat"] = eval(enable_chat) if isinstance(enable_chat, str) else enable_chat
        title = config.get("title")
        if title in role_info:
            config["description"] = role_info[title].get("description")
            config["examples"] = role_info[title].get("examples")
            config["db_name"] = role_info[title].get("db_name")
            config["role_prompt"] = role_info[title].get("role_prompt")
            # Store the original config dictionary
            self._instance._config = config
        else:
            raise Exception(f"{title}-小助手暂不支持，请联系我们～")

    def __getattr__(self, name):
        # Try to get attribute from _config
        if self._instance._config and name in self._instance._config:
            return self._instance._config[name]
        raise AttributeError(f"'SalesConfig' object has no attribute '{name}'")
