from utility import UnreliableSocket, PacketHeader, MSGType
from typing import Tuple, List

NO_ADDRESS = ("None", -1)


class RDTSocket(UnreliableSocket):
    def __init__(self, name: str, reciever_port: int, window_size: int):
        super().__init__()
        self.N = 0
        self.accepted = False
        self.name = name
        self.window_size = window_size
        self.reciever_port = reciever_port
        self.recieved_acks: List[int] = []

    def num_inorder(self) -> int:
        if len(self.recieved_acks) == 0:
            return self.N

        # count = 0
        sorted_acks = (self.recieved_acks.copy())
        sorted_acks.sort()

        for ack in sorted_acks:
            if ack == self.N:
                # count = count + 1
                self.N = self.N + 1
                self.recieved_acks.remove(ack)
            else:
                break

        return self.N

    def accept(self) -> Tuple[bytes, Tuple[str, int]]:
        """Custom accept"""
        (data, address) = self.recv()
        if address == NO_ADDRESS:
            return (data, NO_ADDRESS)

        print(data)
        self.accepted = True
        return (data, address)

    def connect(self, address: Tuple[str, int]):
        self.accepted = True
        self.send(MSGType.START, bytes(), self.N, address)

    def send(self, msgtype: MSGType, data: bytes, seq_num: int, address: Tuple[str, int]):
        length: int = len(data)
        # self.seq_num = self.seq_num + 1

        header: bytes = PacketHeader(msgtype, seq_num, length).to_bytes()
        self.sendto((header.decode() + " " + data.decode()).encode(), address)

    def recv(self) -> Tuple[bytes, Tuple[str, int]]:
        (data, address) = self.recvfrom()

        if data is None or address is None:
            return ("Drop".encode(), NO_ADDRESS)

        ph = PacketHeader(data=data)

        # Packet not within window

        # Already
        if len(self.recieved_acks) > self.window_size:
            return ("Drop".encode(), NO_ADDRESS)

        if ph.verify_packet():
            # Send ACK MSG automatically
            if ph.get_msg_type() != MSGType.ACK:
                print(data)
                # print(self.seq_num)
                # print(self.name)
                print(f'N = {self.N}')
                seq_num = ph.get_seq_num()

                if seq_num == self.N:
                    seq_num = self.num_inorder()
                else:
                    seq_num = self.N

                print(self.N)

                self.send(MSGType.ACK, bytes(), seq_num, address)

            if ph.get_seq_num() > self.N + self.window_size:
                return ("Drop".encode(), NO_ADDRESS)

            if ph.get_msg_type() == MSGType.START:
                # print("Recieved Start MSG")
                return (data, address)

            if self.accepted:
                # print("Recieved Other MSG")
                return (data, address)

        return ("Drop".encode(), NO_ADDRESS)

    def close(self, address: Tuple[str, int]):
        self.send(MSGType.END, bytes(), self.N, address)
