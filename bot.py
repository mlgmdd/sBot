import requests
import json
import asyncio
from post_server import post_server_app
import _thread
import time
import traceback

MAX_MSG_NUMBER = 512
COMMANDS_LIST = ["sum", "s"]


class Bot:
    def __init__(self, config):
        self.uin = config["account"]["uin"]
        self.url = config["http"]["url"]
        self.admins_uin = config["account"]["admin_uin"]
        self.post_server = PostServer()

    def get_group_msg(self, group_id: int, last_msg_seq=None) -> dict:
        # 等价的post由于未知原因不可用:
        # s = json.dumps({"group_id": 603161290})
        # responds = requests.post(self.url + "/get_group_msg_history", data=s)
        responds = requests.get(f"{self.url}/get_group_msg_history?group_id={group_id}", proxies={})
        messages = json.loads(responds.text)["data"]["messages"]
        msg_seq = messages[0]["message_seq"]

        if last_msg_seq is None or msg_seq - last_msg_seq > MAX_MSG_NUMBER:
            last_msg_seq = msg_seq - MAX_MSG_NUMBER

        while msg_seq > last_msg_seq:
            print(f"Getting msg form {group_id}, msg_seq={msg_seq}")
            responds = requests.get(f"{self.url}/get_group_msg_history?group_id={group_id}&message_seq={msg_seq}",
                                    proxies={})
            messages = json.loads(responds.text)["data"]["messages"] + messages
            if msg_seq == messages[0]["message_seq"]:
                break  # 全部读取完毕
            msg_seq = messages[0]["message_seq"]

        return messages

    def send_private_message(self, msg: str, uin: int) -> requests.Response:
        responds = requests.get(f"{self.url}/send_private_msg?user_id={uin}&message={msg}&auto_escape=true",
                                proxies={})
        return responds

    def handle_command_message(self, command: str, sender_uin: int, call_back_func) -> None:
        action, args = self._command_filter(command)
        if action == "not_an_action":
            return
        if action == "invalid_action":
            self.send_private_message("Invalid Command!", sender_uin)
            return
        print(f"Handling Command: {command} from {sender_uin}")
        try:
            call_back_func(action, args, sender_uin)  # 回调App的方法处理用户指令
        except Exception as e:
            self.send_private_message("Error:\n" + str(e), sender_uin)
            traceback.print_exception(e)

    def fetch_command_message(self, call_back_func) -> None:
        rsp = self.post_server.get_data()
        rsp = self._respond_filter(rsp)
        if rsp:
            print(f"Received Data: {rsp}")
            command = rsp["message"]
            sender_uin = rsp["user_id"]
            self.handle_command_message(command, sender_uin, call_back_func)

    def _respond_filter(self, rsp: dict) -> dict:
        if rsp == {} or rsp["post_type"] != "message":
            return {}
        if rsp["user_id"] in self.admins_uin:
            return rsp
        return {}

    @staticmethod
    def _command_filter(cmd: str) -> tuple[str, list]:
        if cmd[0] != '#':
            return "not_an_action", []
        sentence = cmd[1:].split()
        action = sentence[0]
        if action in COMMANDS_LIST:
            arguments = sentence[1:]
            return action, arguments
        else:
            return "invalid_action", []


class PostServer:
    def __init__(self, host="127.0.0.1", port=5701):
        self.host, self.port = host, port
        self.url = f"http://{host}:{port}"
        self.app = post_server_app

    def run(self, debug=False) -> None:
        _thread.start_new_thread(self._server_thread, (debug, self.host, self.port))

    def _server_thread(self, debug, host, port) -> None:
        self.app.run(debug=debug, host=host, port=port)

    def get_data(self) -> dict:
        rsp = json.loads(requests.get(self.url + '/get_data').text)
        return rsp


if __name__ == "__main__":
    from files import AppConfig
    app_config = AppConfig()
    bot = Bot(app_config)
    bot.post_server.run()
    input()










