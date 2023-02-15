import socket
import sys
import signal
from typing import List, Tuple

GREETING: str = "GREETING"
MESSAGE: str = "MESSAGE"
INCOMING: str = "INCOMING"


class Server:

    UDP_IP: str = "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_list: List[Tuple[str]] = []

    def greeting(self, addr: Tuple[str]):
        """Accepts greeting ands adds client to known list"""
        self.client_list.append(addr)

    def message(self, sender: Tuple[str], message_contents: str):
        """Messages all clients from MESSAGE"""
        for client in self.client_list:
            self.s.sendto((INCOMING + " " + str(sender) + ": " + message_contents).encode(), client)

    def main(self, args: List[str]):
        """Initializes Server"""
        # args[1] is port
        self.s.bind((self.UDP_IP, int(args[1])))

        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print("Server Running")
        while True:
            # Recives message and address of sender
            data, addr = self.s.recvfrom(1024)
            # Decodes and splits data
            json = data.decode()
            message_type = json.split(" ")[0]

            # Parses Message
            if message_type == GREETING:
                self.greeting(addr)
            elif message_type == MESSAGE:
                self.message(addr, json.split(" ", 1)[1])
            elif message_type == INCOMING:
                continue
            else:
                print("Unkown message type ignoring message")


Server().main(sys.argv)
