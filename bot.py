import requests
import json

MAX_MSG_NUMBER = 100


class Bot:
    def __init__(self, uin, url):
        self.uin = uin
        self.url = url

    def get_group_msg(self, group_id, last_msg_seq=None):
        # s = json.dumps({"group_id": 603161290})
        # 等价的post由于未知原因不可用
        # responds = requests.post(self.url + "/get_group_msg_history", data=s)
        responds = requests.get(f"{self.url}/get_group_msg_history?group_id={group_id}")
        messages = json.loads(responds.text)["data"]["messages"]
        msg_seq = messages[0]["message_seq"]

        if last_msg_seq is None or msg_seq - last_msg_seq > MAX_MSG_NUMBER:
            last_msg_seq = msg_seq - MAX_MSG_NUMBER

        while msg_seq > last_msg_seq:
            print(f"Getting msg form {group_id}, msg_seq={msg_seq}")
            responds = requests.get(f"{self.url}/get_group_msg_history?group_id={group_id}&message_seq={msg_seq}")
            messages = json.loads(responds.text)["data"]["messages"] + messages
            msg_seq = messages[0]["message_seq"]

        return messages





