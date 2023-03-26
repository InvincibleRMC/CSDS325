from utility import UnreliableSocket, PacketHeader, MSGType
from typing import Tuple


class RDTSocket(UnreliableSocket):
    def __init__(self):
        super().__init__()
        self.seq_num = 0
        self.accepted = False

    def accept(self) -> Tuple[bytes, Tuple[str, int]]:
        """Custom accept"""
        (data, address) = self.recv()
        if address is None:
            return (None, None)

        self.accepted = True
        return (data, address)

    def connect(self, address: Tuple[str, int]):
        self.send(MSGType.START, bytes(), address)

    def send(self, msgtype: MSGType, data: bytes, address: Tuple[str, int]):
        length: int = len(data)
        self.seq_num = self.seq_num + 1
        header: bytes = PacketHeader(msgtype, self.seq_num, length).to_bytes()
        self.sendto((header.decode() + data.decode()).encode(), address)

    def recv(self) -> Tuple[bytes, Tuple[str, int]]:
        (data, address) = self.recvfrom()

        print(str(data) + str(address))
        if data is None or address is None:
            return ("Drop".encode(), None)

        if PacketHeader(data=data).verify_packet():
            if PacketHeader(data=data).get_msg_type != MSGType.ACK:
                self.send(MSGType.ACK, bytes(), address)

            print("ever verified?")

            if PacketHeader(data=data).get_msg_type() == MSGType.START:
                return (data, address)

            if self.accepted:
                return (data, address)

        return ("Drop".encode(), None)

    def close(self, address: Tuple[str, int]):
        self.send(MSGType.END, bytes(), address)
