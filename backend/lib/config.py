import os

import yaml


class Config:
    def __init__(self):
        "Initialize empty configuration set"
        self._cfg = {}

        self.config_path = None

    def load_from_yaml(self, config_path, globbing=False):
        "Load configuration options from YAML file"
        with open(config_path, "r") as f:
            loaded = yaml.load(f)
            self._cfg.update(loaded)

            self.config_path = os.path.dirname(config_path)

    def get(self, key):
        keys = key.split(".")

        current_lvl = self._cfg

        for _key in keys:
            if not isinstance(current_lvl, dict):
                raise KeyError(key)

            current_lvl = current_lvl.get(_key)

            if current_lvl is None:
                raise KeyError(key)

        return current_lvl
