# -- coding: utf-8 --
from flask import Flask
import requests
import time

from files import LocalData, AppConfig
from gpt import Gpt
from bot import Bot
import _thread


GAP = 1


class App:
    def __init__(self):
        self.config = AppConfig("./config.yml")
        self.uin = self.config["account"]["uin"]
        self.local_data = LocalData(self.uin)
        self.gpt = Gpt(self.config["gpt"]["api-key"], self.config["gpt"]["model"])
        self.bot = Bot(self.config)

        # self.refresh_groups_msg()

        self.gap = 0

    def refresh_groups_msg(self):
        data = {}
        for group_id in self.local_data.group_info.keys():
            msgs = self.bot.get_group_msg(group_id)
            data[group_id] = msgs
        self.local_data.save_group_msg(data)

    def get_summary(self, group_id: int) -> str:
        prompts = [
            {"role": "system", "content": self.config["gpt"]["prompt"]["system"]},
            {"role": "user", "content": self.config["gpt"]["prompt"]["user"] + '\n'}
        ]
        messages = self.gpt.format_gpt_message(self.local_data.group_history_msg[str(group_id)])
        prompts[1]["content"] += messages
        print(f"发出请求... (长度{len(messages)})")

        r = self.gpt.summarize(prompts)
        return r

    def exec_command(self, action: str, args: list, sender_uin: int):
        if action == "sum" or action == "s":
            r = self.get_summary(group_id=args[0])
            self.bot.send_private_message(r, sender_uin)

    def main_loop(self):
        self.bot.post_server.run()
        while True:
            if self.timer():
                # self.refresh_groups_msg()
                pass
            print(self.gap)
            self.bot.fetch_command_message(self.exec_command)
            time.sleep(1)

    def timer(self):
        if self.gap >= self.config["bot"]["refresh_interval"]:
            self.gap = 0
            return True
        self.gap += 1
        return False


