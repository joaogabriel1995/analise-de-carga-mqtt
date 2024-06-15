import sys
sys.path.append('../')

from  message.message import MessageHandler
class RoundTripTime():
    def __init__(self, message_handler: MessageHandler) -> None:
        self.message_handler = message_handler

    def calculate(self):
        rtt = (self.message_handler.receive_time - self.message_handler.send_time ) * 1000
        return rtt

