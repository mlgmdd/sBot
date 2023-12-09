from openai import OpenAI


class Gpt:
    def __init__(self, api_key, model):
        self.client = OpenAI()
        self.api_key = api_key
        self.model = model

    def summarize(self, messages):
        """
        messages = [
                {"role": "system",
                 "content": "You are a poetic assistant, skilled in explaining complex programming concepts with \
                 creative flair."},
                {"role": "user",
                "content": "Compose a poem that explains the concept of recursion in programming."}
            ]
            """
        completion = self.client.chat.completions.create(model=self.model, messages=messages)
        return completion.choices[0].message.content

    @staticmethod
    def format_gpt_message(messages) -> str:
        format_messages = ""
        for msg in messages:
            content = msg["message"]
            if content[0] == '[':
                continue
            sender_nickname = msg["sender"]["nickname"]
            t = f"{sender_nickname}: {content}/n"
            format_messages += t
        return format_messages

