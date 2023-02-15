import socket
import signal
import sys
from typing import List
from threading import Thread

GREETING: str = "GREETING"
MESSAGE: str = "MESSAGE"
INCOMING: str = "INCOMING"


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_init_message(self):
        """Sends GREETING message"""
        message: str = GREETING
        self.s.sendto(message.encode(), self.ip_port)

    def send_message(self):
        """Sends MESSAGE message"""
        while True:
            print("Send a message!")
            msg: str = MESSAGE + " " + input()
            self.s.sendto(msg.encode(), self.ip_port)

    def recieve_incoming(self):
        """Recieves INCOMING message"""
        while True:
            data = self.s.recv(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]
            if message_type == INCOMING:
                print(message_contents)
            else:
                print("Invalid Server Message")

    def main(self, args: List[str]):
        """Starts Client"""
        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.ip_port = tuple((args[1], int(args[2])))
        self.send_init_message()

        # Creates threads to avoid blocking
        Thread(target=self.send_message).start()
        Thread(target=self.recieve_incoming).start()


Client().main(sys.argv)
