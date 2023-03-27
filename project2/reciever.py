from rdtscocket import RDTSocket
from typing import List
import sys
from utility import PacketHeader, MSGType
import signal


class Reciever():

    def __init__(self, args: List[str]):
        if len(args) != 3:
            raise SystemError()

        self.s = RDTSocket()
        self.reciever_port = int(args[1])
        self.window_size = int(args[2])

        self.s.bind(("localhost", self.reciever_port))
        self.recieved_window: List[bool] = [False]*self.window_size

        while not self.s.accepted:
            self.s.accept()
        print("Connection Accepted!")

        with open("download.txt", "w") as f:

            while True:
                (data, addr) = self.s.recv()

                # print(data)
                if data.decode() == "Drop":
                    continue

                if PacketHeader(data=data).get_msg_type() == MSGType.END:
                    break

                if PacketHeader(data=data).get_msg_type() != MSGType.DATA:
                    continue

                if PacketHeader(data=data).get_seq_num() > self.s.seq_num + self.window_size:
                    continue

                text = data.decode().split(" ", maxsplit=4)
                print(text)
                if len(text) == 20:
                    f.write("\n")
                else:
                    f.write(f'{text[4]}\n')

        print("Recieved Download!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Reciever(sys.argv)
