from rdtscocket import RDTSocket
from typing import List, Dict
import sys
from utility import PacketHeader, MSGType
import signal


class Reciever():

    def __init__(self, args: List[str]):
        if len(args) != 3:
            raise SystemError()

        self.s = RDTSocket("Reciever", int(args[1]), int(args[2]))
        self.s.bind(("localhost", self.s.reciever_port))
        self.previous_msgs: Dict[int, str] = {}
        print("Started Reciever!")

        while not self.s.accepted:
            self.s.accept()
        print("Connection Accepted!")

        self.s.N = 0

        while True:
            data, addr = self.s.recv()

            print(f'Recieved {data}')
            if data.decode() == "Drop":
                continue

            if PacketHeader(data=data).get_msg_type() == MSGType.END:
                break

            if PacketHeader(data=data).get_msg_type() != MSGType.DATA:
                continue

            text = data.decode().split(" ", maxsplit=4)
            ack_num = int(text[1])
            msg = text[4]

            # Skip Dupes
            if self.previous_msgs.get(ack_num) is not None:
                continue

            self.s.recieved_acks.append(ack_num)
            self.previous_msgs.update({ack_num: msg})

        with open("download.txt", "w") as f:
            sorted_list: List[int] = []

            for key in self.previous_msgs.keys():
                sorted_list.append(key)

            sorted_list.sort()
            for ack in sorted_list:
                msg = self.previous_msgs.get(ack)
                if isinstance(msg, str):
                    f.write(f'{msg}\n')
            print("Recieved Download!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Reciever(sys.argv)
