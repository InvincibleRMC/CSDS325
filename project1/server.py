"""Server for CWRU Plan+"""
import socket
import sys
import time
import signal
from typing import List, Tuple

GREETING: str = "GREETING"
MESSAGE: str = "MESSAGE"
INCOMING: str = "INCOMING"


class Server:

    UDP_IP: str = "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_list: List[Tuple[str]] = []

    def greeting(self, message_contents: Tuple[str]):
        self.client_list.append(message_contents)

    def message(self, message_contents: str):
        for client in self.client_list:
            self.s.sendto((INCOMING + " " + str(client) + " " + message_contents).encode(), client)
            print("Finished Sending INCOMING")

    def main(self, args: List[str]):
        udp_port_num: int = int(args[1])

        self.s.bind((self.UDP_IP, udp_port_num))

        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        while 1:
            data, addr = self.s.recvfrom(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]

            if message_type == GREETING:
                self.greeting(addr)
            elif message_type == MESSAGE:
                self.message(message_contents)
            elif message_type == INCOMING:
                continue
            else:
                print("Unkown message type ignoring message")

        self.s.close()


Server().main(sys.argv)
