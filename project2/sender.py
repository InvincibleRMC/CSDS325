from rdtscocket import RDTSocket
from typing import List
import sys
from utility import PacketHeader, MSGType
import signal
import time


class Sender():

    def __init__(self, args: List[str]):
        if len(args) != 4:
            raise SystemError()

        self.s = RDTSocket()
        self.reciever_ip = args[1]
        self.reciever_port = int(args[2])
        self.window_size = int(args[3])

        address = (self.reciever_ip, self.reciever_port)

        self.recieved_window: List[bool] = [False]*self.window_size

        while True:
            self.s.connect(address)
            (data, addr) = self.s.recv()
            # print(data)
            if data.decode() == "Drop":
                continue
            break

        print("Connection Acknowledged")

        with open("alice.txt", "r") as f:
            text = f.read().splitlines()
            linetotal = len(text)
            # counter = 0
            while True:

                for i in range(self.window_size):
                    if self.recieved_window[i]:
                        self.recieved_window.pop()
                        self.s.seq_num = self.s.seq_num + 1
                        self.recieved_window.insert(self.window_size, False)
                    else:
                        break

                assert len(self.recieved_window) == self.window_size

                if self.s.seq_num >= linetotal:
                    self.s.close(address)
                    (data, addr) = self.s.recv()
                    if data.decode() == "Drop":
                        continue

                    packetHeader = PacketHeader(data=data)
                    if packetHeader.get_seq_num() == self.s.seq_num and packetHeader.get_msg_type() == MSGType.ACK:
                        break
                else:
                    for i in range(self.window_size):
                        if self.s.seq_num >= linetotal:
                            continue
                        print(f'Sending {text[self.s.seq_num + i].encode()}!')
                        self.s.send(MSGType.DATA, text[i].encode(), address)

                (data, addr) = self.s.recv()
                print(data)
                if data.decode() == "Drop":
                    continue
                else:
                    self.recieved_window[PacketHeader(data=data).get_seq_num() % self.window_size] = True

                time.sleep(0.5)
        print("Sent File!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Sender(sys.argv)
