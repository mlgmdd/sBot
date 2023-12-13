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

        self.group_history_msg_path = self.user_data_path + 'group_history_msg.json'

        self.group_history_msg = self._load_file(self.group_history_msg_path)
        self.group_info = self._load_file(self.user_data_path + 'group_info.json')

    @staticmethod
    def _load_file(file_path: str) -> dict:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump({}, file)

        with open(file_path, 'r') as file:
            data = json.load(file)
            return data

    def save_group_msg(self, messages, group_id) -> None:
        file_path = self.group_history_msg_path
        self.group_history_msg[str(group_id)] = messages
        print(f"Saving group {group_id} messages at {file_path}")
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(self.group_history_msg, file)

    def clear_group_msg(self, group_id: int) -> None:
        self.save_group_msg([], group_id)


class AppConfig:
    def __init__(self, path="./config.yml"):
        self.path = path
        self.config_dict = self._read_app_config_file()
        self._missing_check()

    def _read_app_config_file(self) -> dict:
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


