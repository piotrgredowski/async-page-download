import yaml


class Config:
    def __init__(self):
        self._cfg = {}

    def load_from_yaml(self, config_path):
        "Load configuration options from YAML file"
        with open(config_path, "r") as f:
            loaded = yaml.load(f)
            self._cfg.update(loaded)

    def get(self, key):
        """
        Allows to get nested key from configuration

        Args:
            key (str): simple 'key' or path to nested key 'key.child_key_1.child_key_2'

        Raises:
            KeyError: when key doesn't exist in configuration

        Returns:
            str or int or float: value of given configuration key
        """

        keys = key.split(".")

        current_lvl = self._cfg

        for _key in keys:
            if not isinstance(current_lvl, dict):
                raise KeyError(key)

            current_lvl = current_lvl.get(_key)

            if current_lvl is None:
                raise KeyError(key)

        return current_lvl
