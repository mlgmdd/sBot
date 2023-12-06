# -- coding: utf-8 --
from flask import Flask
import requests

from files import LocalData, AppConfig


class Bot:
    def __init__(self):
        self.config = AppConfig("./config.yml")
        self.uin = self.config["account"]["uin"]
        self.local_data = LocalData(self.uin)


if __name__ == "__main__":
    app = Bot()

