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

        self.s = RDTSocket("Sender", int(args[2]), int(args[3]))
        self.reciever_ip = args[1]
        # self.reciever_port =
        # self.window_size = )

        address = (self.reciever_ip, self.s.reciever_port)

        # self.sent: List[int] = []
        # self.recieved_window: List[int] = [-1]*self.s.window_size
        # self.recieved: List[int] = []

        print("Started Sender!")
        while True:
            self.s.connect(address)
            (data, addr) = self.s.recv()
            print(data)
            if data.decode() == "Drop":
                continue
            break

        print("Connection Acknowledged")

        # counter = 1
        self.s.N = 0

        with open("alice.txt", "r") as f:
            text = f.read().splitlines()
            linetotal = len(text)
            # counter = 0
            while True:
                # print(self.s.N)
                # print(self.msgs)

                # for i in range(self.window_size):

                #     if len(self.msgs) > 0:

                #         if self.recieved_window[i] == self.msgs[0]:
                #             self.recieved_window[i] = -1
                #             self.msgs.pop()
                #             self.s.seq_num = self.s.seq_num + 1
                #             # self.recieved_window.insert(self.window_size, False)
                #         else:
                #             break

                # assert len(self.recieved_window) == self.window_size

                if self.s.N >= linetotal:
                    self.s.close(address)
                    (data, addr) = self.s.recv()
                    if data.decode() == "Drop":
                        continue

                    # packetHeader =
                    if PacketHeader(data=data).get_msg_type() == MSGType.ACK:
                        break
                else:
                    for i in range(self.s.window_size):
                        seq_num = self.s.N + i
                        # print(seq_num)
                        if seq_num >= linetotal:
                            continue
                        if text[seq_num] == " ":
                            text[seq_num] = "\n"

                        msg: bytes = text[seq_num].encode()
                        print(f'Sending {msg}!')
                        # self.msgs.append(seq_num)
                        self.s.send(MSGType.DATA, msg, seq_num, address)

                # 
                # self.sent.sort()

                (data, addr) = self.s.recv()
                print(f'Recieved {data}')
                if data.decode() == "Drop":
                    continue
                else:
                    seq_num = PacketHeader(data=data).get_seq_num()
                    if seq_num != self.s.N:
                        self.s.N = seq_num
                        continue
                    
                    # if self.msgs.count(seq_num) > 0:
                    #     self.msgs.remove(seq_num)

                # time.sleep(0.5)
                # self.msgs.clear()
        print("Sent File!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Sender(sys.argv)
