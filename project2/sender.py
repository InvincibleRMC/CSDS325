from rdtscocket import RDTSocket
from typing import List
import sys
from utility import PacketHeader, MSGType
import signal


class Sender():

    def __init__(self, args: List[str]):
        if len(args) != 4:
            raise SystemError()

        self.s = RDTSocket()
        self.reciever_ip = args[1]
        self.reciever_port = int(args[2])
        self.window_size = int(args[3])

        address = (self.reciever_ip, self.reciever_port)

        while True:
            self.s.connect(address)
            (data, addr) = self.s.recv()
            print(data)
            if data.decode() == "Drop":
                continue

            packetHeader = PacketHeader(data=data)
            print(packetHeader.get_seq_num())
            print(self.s.seq_num)
            if packetHeader.get_seq_num() == self.s.seq_num and packetHeader.get_msg_type() == MSGType.ACK:
                break

        print("Connection Acknowledged")

        with open("alice.txt", "r") as f:
            text = f.read().splitlines()
            print(text)
            return
            linetotal = len(text)
            counter = 0
            while True:
                counter = counter + 1
                if counter == linetotal:
                    self.s.close(address)
                    (data, addr) = self.s.recv()
                    packetHeader = PacketHeader(data=data)
                    if packetHeader.get_seq_num() == self.s.seq_num and packetHeader.get_msg_type() == MSGType.ACK:
                        break

                print(f'Sending {text[counter].encode()}!')
                self.s.send(MSGType.DATA, text[counter].encode(), address)
                # f.write(text)

        print("Sent File!")


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)
Sender(sys.argv)
