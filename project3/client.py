import socket
import sys
from typing import List, Dict
from constants import PORT_ADDRESS, JOIN, UPDATE, INCOMING, Pairs, str_to_pair_list


class Client:

    def __init__(self, name: str, dv: Dict[str, int] = {}):
        self.ip_port = PORT_ADDRESS
        self.name = name
        self.dv: Dict[str, int] = dv
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_join_message(self):
        """Sends JOIN message"""
        message: str = JOIN + " " + self.name
        self.s.sendto(message.encode(), self.ip_port)

    def __str__(self):
        return f'Client {self.name} has DV = {self.dv}'

    def send_update(self):
        pair_list: List[Pairs] = []
        for keys in self.dv.keys():
            pair_list.append(Pairs(keys, self.dv[keys]))

        new_msg: str = UPDATE + " " + self.name + " " + str(pair_list)
        self.s.sendto(new_msg.encode(), self.ip_port)

    def handle_incoming(self, msg: str):
        splitted = msg.split(" ", 1)
        name = splitted[0]
        pair_list = str_to_pair_list(splitted[1])
        new_dv: Dict[str, int] = {}

        if name == self.name:
            for pair in pair_list:
                new_dv[pair.Node] = sys.maxsize if pair.cost == -1 else pair.cost
            if self.dv == {}:
                self.dv = new_dv.copy()
                print(f"Sending Init Update from {self.name}")
                self.send_update()
        else:
            new_dv = self.dv.copy()
            for pair in pair_list:
                new_dv[pair.Node] = min(new_dv[pair.Node], pair.cost + self.dv[name])

            assert len(self.dv) == len(new_dv)
            for keys in self.dv.keys():
                if self.dv[keys] != new_dv[keys]:
                    self.dv = new_dv.copy()
                    self.send_update()
                    return

            print(f'from {name} {new_dv}')
            print(f"{self.name} done updating with DV table = {self.dv}")

    def receive_incoming(self):
        """Receives INCOMING message"""
        while True:
            data = self.s.recv(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]
            if message_type == INCOMING:
                self.handle_incoming(message_contents)
            else:
                print("Invalid Server Message")

    def main(self):
        """Starts Client"""
        self.send_join_message()
        self.receive_incoming()
