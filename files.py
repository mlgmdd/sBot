# -- coding: utf-8 --
import json
import yaml
import os


class LocalData:
    def __init__(self, uin: int):
        self.data_path = './data/'
        self.user_data_path = self.data_path + str(uin) + '/'
        self.uin = uin

        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)

        self.group_history_msg = self._load_file(self.user_data_path + 'group_history_msg.json')
        self.group_info = self._load_file(self.user_data_path + 'group_info.json')

    @staticmethod
    def _load_file(file_path: str):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({}, file)

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                return None

    def save_group_msg(self, data):
        file_path = self.user_data_path + 'group_history_msg.json'
        print(f"Saving group messages at {file_path}")
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file)




class AppConfig:
    def __init__(self, path="./config_dict.yml"):
        self.path = path
        self.config_dict = self.read_app_config_file()

    def read_app_config_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            raise Exception("Config File Not found")
        except yaml.YAMLError as exc:
            raise Exception(f"Config File: {exc}")

    def _missing_check(self):
        if not self.config_dict["account"]["uin"]:
            raise Exception("Config: uin Not Found")
        if not self.config_dict["gpt"]["api-key"]:
            raise Exception("Config: api-key Not Found")

    def __getitem__(self, item):
        return self.config_dict[item]


