# -- coding: utf-8 --
from flask import Flask
import requests
import time

from files import LocalData, AppConfig
from gpt import Gpt
from bot import Bot


GAP = 1

class App:
    def __init__(self):
        self.config = AppConfig("./config.yml")
        self.uin = self.config["account"]["uin"]
        self.local_data = LocalData(self.uin)
        self.gpt = Gpt(self.config["gpt"]["api-key"], self.config["gpt"]["model"])
        self.bot = Bot(self.uin, self.config["http"]["url"])

        # self.refresh_groups_msg()

        self.gap = 0

    def refresh_groups_msg(self):
        data = {}
        for group_id in self.local_data.group_info.keys():
            msgs = self.bot.get_group_msg(group_id)
            data[group_id] = msgs
        self.local_data.save_group_msg(data)

    def get_summary(self, group_id):
        prompts = [
            {"role": "system", "content": self.config["gpt"]["prompt"]["system"]},
            {"role": "user", "content": self.config["gpt"]["prompt"]["user"] + '\n'}
        ]
        messages = self.gpt.format_gpt_message(self.local_data.group_history_msg[str(group_id)])
        prompts[1]["content"] += messages
        print(f"发出请求... (长度{len(messages)})")
        return self.gpt.summarize(prompts)

    def main_loop(self):

        if self.timer():
            self.refresh_groups_msg()

    def timer(self):
        if self.gap == GAP:
            self.gap = 0
            return True
        time.sleep(1)
        self.gap += 1
        return False


