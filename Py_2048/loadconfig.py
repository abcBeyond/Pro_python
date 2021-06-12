import yaml
import json


class ConfigYaml:
    def __init__(self, file_name):
        self.config_file = file_name
        self.yaml_value = None
        self.load()

    def load(self):
        with open(self.config_file, encoding="utf-8") as f:
            self.yaml_value = yaml.load(f, Loader=yaml.FullLoader)

    def get(self):
        return self.yaml_value
