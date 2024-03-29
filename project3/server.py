import socket
import signal
from typing import Dict, Tuple

from constants import PORT_ADDRESS, JOIN, UPDATE, INCOMING, STARTING_CONFIG, str_to_pair_list


class Server:

    def __init__(self):
        """Server Constructor"""
        self.ip_port = PORT_ADDRESS
        self.config = STARTING_CONFIG

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_list: Dict[str, Tuple[str]] = {}

    def greeting(self, addr: Tuple[str], name: str):
        """Accepts greeting ands adds client to known list"""
        self.client_list[name] = addr
        print(self.client_list)

        if len(self.client_list) == len(self.config):

            # Hopefully doesn't get triggered but sometimes UDP ports would not be unique
            hash_val: Dict[Tuple[str], bool] = dict()
            for keys in self.client_list:
                if self.client_list[keys] in hash_val:
                    raise Exception("UDP ports are not unique please restart computer.")
                else:
                    hash_val[self.client_list[keys]] = True

            for node_name in self.client_list.keys():
                client = self.client_list[node_name]
                msg = self.config[node_name]
                self.s.sendto((INCOMING + " " + node_name + " " + str(msg)).encode(), client)

    def update(self, message_contents: str):
        """Propagates update to neighbors"""
        splitted = message_contents.split(" ", 1)
        node_name = splitted[0]
        message_contents = splitted[1]
        pair_list = str_to_pair_list(message_contents)
        for pair in self.config[node_name]:
            if pair.cost != -1:
                self.s.sendto((INCOMING + " " + node_name + " " + str(pair_list)).encode(), self.client_list[pair.Node])

    def main(self):
        """Initializes Server"""
        self.s.bind(self.ip_port)

        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        print("Server Running")
        while True:
            # Receives message and address of sender
            data, addr = self.s.recvfrom(1024)
            # Decodes and splits data
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]

            # Parses Message
            if message_type == JOIN:
                self.greeting(addr, message_contents)
            elif message_type == INCOMING:
                continue
            elif message_type == UPDATE:
                self.update(message_contents)
            else:
                print("Unknown message type ignoring message")


Server().main()
