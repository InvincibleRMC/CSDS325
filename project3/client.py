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
        self.dv: Dict[str, int] = {}

    def send_join_message(self):
        """Sends JOIN message"""
        message: str = JOIN + " " + self.name
        self.s.sendto(message.encode(), self.ip_port)

    # def send_update_input(self):
    #     """Sends UPDATE message"""
    #     while True:
    #         print("Send a update!")
    #         msg: str = UPDATE + " " + input()
    #         self.s.sendto(msg.encode(), self.ip_port)

    def send_update(self):
        pair_list: List[Pairs] = []
        for keys in self.dv.keys():
            pair_list.append(Pairs(keys, self.dv[keys]))

        new_msg: str = UPDATE + " " + self.name + " " + str(pair_list)
        self.s.sendto(new_msg.encode(), self.ip_port)

    def handle_incoming(self, msg: str):
        # print("HERE")
        # print(msg)
        splitted = msg.split(" ", 1)
        name = splitted[0]
        pair_list = str_to_pair_list(splitted[1])
        new_dv: Dict[str, int] = {}

        if name == self.name:
            for pair in pair_list:
                new_dv[pair.Node] = pair.cost
            # Add itself as dist 0
            new_dv[self.name] = 0
            self.dv = new_dv.copy()
            print("Sending Init Update")
            self.send_update()
        else:
            new_dv = self.dv
            for keys in self.dv.keys():
                for pair in pair_list:
                    if pair.cost == -1:
                        pair.cost = sys.maxsize

                    new_dv[keys] = min(new_dv[keys], pair.cost + self.dv[pair.Node])

            assert len(self.dv) == len(new_dv)
            for keys in self.dv.keys():
                if self.dv[keys] != new_dv[keys]:
                    self.dv = new_dv.copy()
                    self.send_update()
                    break
            print(f"{self.name} done updating with DV table = {self.dv}")

    def recieve_incoming(self):
        """Recieves INCOMING message"""
        while True:
            data = self.s.recv(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]
            if message_type == INCOMING:
                self.handle_incoming(message_contents)
                print(self.dv)
            else:
                print("Invalid Server Message")

    def main(self):
        """Starts Client"""
        # Kills with Control + C
        # signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.send_join_message()

        # Creates threads to avoid blocking
        # Thread(target=self.send_upeedate_input).start()
        # Thread(target=self.recieve_incoming).start()
        self.recieve_incoming()


# Client(sys.argv).main()
