import socket
import signal
import sys
from typing import List, Dict
from threading import Thread
from constants import PORT_ADDRESS, JOIN, UPDATE, INCOMING, Pairs, str_to_pair_list


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, name: List[str]):
        self.ip_port = PORT_ADDRESS
        if len(name) != 2:
            raise Exception
        self.name = name[1]
        self.info: Dict[str, List[Pairs]] = {}

    def send_join_message(self):
        """Sends JOIN message"""
        message: str = JOIN + " " + self.name
        self.s.sendto(message.encode(), self.ip_port)

    def send_update(self):
        """Sends UPDATE message"""
        while True:
            print("Send a update!")
            msg: str = UPDATE + " " + input()
            self.s.sendto(msg.encode(), self.ip_port)

    def handle_incoming(self, msg: str):
        splitted = msg.split(" ", 1)
        name = splitted[0]
        self.info[name] = str_to_pair_list(splitted[1])

    def recieve_incoming(self):
        """Recieves INCOMING message"""
        while True:
            data = self.s.recv(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]
            if message_type == INCOMING:
                self.handle_incoming(message_contents)
                # TODO run DV
                print(self.info)
            else:
                print("Invalid Server Message")

    def main(self):
        """Starts Client"""
        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.send_join_message()

        # Creates threads to avoid blocking
        Thread(target=self.send_update).start()
        Thread(target=self.recieve_incoming).start()


Client(sys.argv).main()
