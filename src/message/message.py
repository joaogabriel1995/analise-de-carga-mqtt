import string
import random
import time


class MessageHandler(object):
    def __init__(
        self,
        type: str,
        qos: int,
        topic: str,
        timeout: int,
        name: str,
        message_count: int,
        size: int,
    ):
        self.type = type
        self.qos = qos
        self.topic = topic
        # self.send_time = send_time

        self.timeout = timeout
        self.name = name
        self.message_count = message_count
        self.create_payload(size)

        self.receive_time = 0
        self.send_time = 0


    def create_payload(self, size: int):
        self.payload = "".join(
            random.choice(string.ascii_lowercase) for _ in range(size)
        )
        return self.payload.encode("utf-8")

    def get_message_count(self):
        return self.message_count

    def increment_message_count(self):
        self.message_count += 1
        return self.message_count

    def insert_receive_time(self):
        self.receive_time = time.monotonic()

    def insert_send_time(self):
        self.send_time = time.monotonic()


if __name__ == "__main__":
    message = MessageHandler(
        "Round Trip Time", 1, "topic", 1, 1, "mensagem name", 0, 10
    )
    message.insert_receive_time()
    print(message.receive_time)
