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
        # self.reciever_port =
        # self.window_size = int(args[2])

        self.s.bind(("localhost", self.s.reciever_port))
        # self.recieved_window: List[bool] = [False]*self.s.window_size
        self.previous_msgs: Dict[int, str] = {}
        print("Started Reciever!")

        while not self.s.accepted:
            self.s.accept()
        print("Connection Accepted!")
        # self.recieved
        self.s.N = 0

        while True:
            print(self.s.N)
            print(self.s.recieved_acks)
            (data, addr) = self.s.recv()

            # print(self.previous_msgs)
            print(data)
            if data.decode() == "Drop":
                continue

            if PacketHeader(data=data).get_msg_type() == MSGType.END:
                break

            if PacketHeader(data=data).get_msg_type() != MSGType.DATA:
                continue

            # if PacketHeader(data=data).get_seq_num() > self.s.seq_num + self.window_size:
            #     continue

            # self.s.seq_num = self.s.seq_num + 1
            text = data.decode().split(" ", maxsplit=4)
            ack_num = int(text[1])
            msg = text[4]

            print(ack_num)
            print(self.s.N)
            # Skip Dupes
            if self.previous_msgs.get(ack_num) is not None:
                continue
            print("after continue")
            self.s.recieved_acks.append(ack_num)
            # if len(text) == -1:
            #     f.write("\n")
            # else:
            # print(f'Wrote {msg} to file.')
            # f.write(f'{msg}\n')
            # f.flush()
            self.previous_msgs.update({ack_num: msg})

        with open("download.txt", "w") as f:

            print(self.previous_msgs)
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
