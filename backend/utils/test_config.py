import unittest
from unittest.mock import (
    MagicMock,
    mock_open,
    patch,
)

import yaml

from utils import Config


class TestConfig(unittest.TestCase):
    "Tests for Config"

    def setUp(self):
        self.config = Config()

    def test_load_from_yaml(self):
        "Test loading config file from yaml file"
        mocked_config = {
            "key": "value"
        }

        with patch('__main__.open', mock_open()):
            yaml.load = MagicMock(return_value=mocked_config)

        self.config.load_from_yaml("config.yml")

        yaml.load.assert_called_once()
        self.assertEqual(self.config._cfg, mocked_config)

    def test_get(self):
        "Test getting keys from config"
        mocked_config = {
            "app": {
                "server": {
                    "host": "1.2.3.4"
                },
                "name": "Test App"
            },
            "key": "value",
        }
        self.config._cfg = mocked_config

        # Test getting simple key
        result_key = self.config.get("key")

        self.assertEqual(result_key, mocked_config["key"])

        # Test getting nested key
        result_nested_key = self.config.get("app.server")

        self.assertEqual(result_nested_key, mocked_config["app"]["server"])

        # Test getting nested key
        result_nested_key = self.config.get("app.server.host")

        self.assertEqual(result_nested_key,
                         mocked_config["app"]["server"]["host"])

        with self.assertRaises(KeyError):
            self.config.get("wrong_key")
