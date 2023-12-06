# -- coding: utf-8 --
from flask import Flask
import requests

from files import LocalData, AppConfig
from gpt import Gpt
from bot import Bot


class App:
    def __init__(self):
        self.config = AppConfig("./config.yml")
        self.uin = self.config["account"]["uin"]
        self.local_data = LocalData(self.uin)
        self.gpt = Gpt(self.config["gpt"]["api-key"], self.config["gpt"]["model"])
        self.bot = Bot(self.uin, self.config["http"]["url"])


if __name__ == "__main__":
    app = App()
    msgs = app.bot.get_group_msg(group_id=603161290)
    # app.local_data.save_group_msg(msgs)
    print(msgs)

