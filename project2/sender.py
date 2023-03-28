from rdtscocket import RDTSocket
from typing import List
import sys
from utility import PacketHeader, MSGType
import signal


class Sender():

    def __init__(self, args: List[str]):
        if len(args) != 4:
            raise SystemError()

        self.s = RDTSocket("Sender", int(args[2]), int(args[3]))
        self.reciever_ip = args[1]
        address = (self.reciever_ip, self.s.reciever_port)

        print("Started Sender!")
        while True:
            self.s.connect(address)
            data, addr = self.s.recv()
            print(data)
            if data.decode() == "Drop":
                continue
            break

        print("Connection Acknowledged")
        self.s.N = 0

        with open("alice.txt", "r") as f:
            text = f.read().splitlines()
            linetotal = len(text)
            while True:

                if self.s.N >= linetotal:
                    self.s.close(address)
                    data, addr = self.s.recv()
                    if data.decode() == "Drop":
                        continue
                    if PacketHeader(data=data).get_msg_type() == MSGType.END_ACK:
                        break
                else:
                    for i in range(self.s.window_size):
                        seq_num = self.s.N + i
                        # Limits send amount when end of file reached
                        if seq_num >= linetotal:
                            continue
                        if text[seq_num] == " ":
                            text[seq_num] = "\n"


                        msg: bytes = text[seq_num].encode()
                        print(f'Sending {msg}!')
                        self.s.send(MSGType.DATA, msg, seq_num, address)

                data, addr = self.s.recv()
                print(f'Recieved {data}')
                if data.decode() == "Drop":
                    continue
                # Extra Redundancy
                elif PacketHeader(data=data).get_msg_type() == MSGType.END_ACK:
                    break
                else:
                    seq_num = PacketHeader(data=data).get_seq_num()
                    if seq_num != self.s.N:
                        self.s.N = seq_num
                        continue

        print("Sent File!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Sender(sys.argv)
