from rdtscocket import RDTSocket
from typing import List
import sys
from utility import PacketHeader, MSGType
import signal


class Reciever():

    def __init__(self, args: List[str]):
        if len(args) != 3:
            raise SystemError()

        self.s = RDTSocket("Reciever")
        self.reciever_port = int(args[1])
        self.window_size = int(args[2])

        self.s.bind(("localhost", self.reciever_port))
        self.recieved_window: List[bool] = [False]*self.window_size
        self.previous_msgs: List[int] = []
        print("Started Reciever!")

        while not self.s.accepted:
            self.s.accept()
        print("Connection Accepted!")

        with open("download.txt", "w") as f:

            while True:
                (data, addr) = self.s.recv()

                # print(self.previous_msgs)
                print(data)
                if data.decode() == "Drop":
                    continue

                if PacketHeader(data=data).get_msg_type() == MSGType.END:
                    break

                if PacketHeader(data=data).get_msg_type() != MSGType.DATA:
                    continue

                if PacketHeader(data=data).get_seq_num() > self.s.seq_num + self.window_size:
                    continue

                self.s.seq_num = self.s.seq_num + 1
                text = data.decode().split(" ", maxsplit=4)
                ack_num = int(text[1])
                msg = text[4]

                if self.previous_msgs.count(ack_num) > 0:
                    continue

                if len(text) == -1:
                    f.write("\n")
                else:
                    print(f'Wrote {msg} to file.')
                    f.write(f'{msg}\n')
                    f.flush()
                    self.previous_msgs.append(int(ack_num))

        print("Recieved Download!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Reciever(sys.argv)
