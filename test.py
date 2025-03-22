class Ultrawebhook:
    def __init__(self, json):
        self.json = json
        self.dict_messages = json["data"]

    def processing(self):
        if self.dict_messages:
            message = self.dict_messages
            sender_number = message["from"]
            received_text = message["body"]
            print(f"Sender: {sender_number}, Message: {received_text}")
            return ""
