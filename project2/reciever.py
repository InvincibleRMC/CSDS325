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

        while not self.s.accepted:
            self.s.accept()
        print("Connection Accepted!")

        with open("download.txt", "w") as f:

            while True:
                (data, addr) = self.s.recv()

                print(data)
                if data.decode() == "Drop":
                    continue

                if PacketHeader(data=data).get_msg_type() == MSGType.END:
                    break

                if PacketHeader(data=data).get_msg_type() != MSGType.DATA:
                    continue

                text = data.decode().split(" ", maxsplit=5)
                print(text)
                f.write(text[5])

        print("Recieved Download!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Reciever(sys.argv)
