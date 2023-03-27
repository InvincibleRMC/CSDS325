from utility import UnreliableSocket, PacketHeader, MSGType
from typing import Tuple

NO_ADDRESS = ("None", -1)


class RDTSocket(UnreliableSocket):
    def __init__(self, name: str):
        super().__init__()
        self.seq_num = 0
        self.accepted = False
        self.name = name

    def accept(self) -> Tuple[bytes, Tuple[str, int]]:
        """Custom accept"""
        (data, address) = self.recv()
        if address == NO_ADDRESS:
            return (data, NO_ADDRESS)

        self.accepted = True
        return (data, address)

    def connect(self, address: Tuple[str, int]):
        self.accepted = True
        self.send(MSGType.START, bytes(), address)

    def send(self, msgtype: MSGType, data: bytes, address: Tuple[str, int]):
        length: int = len(data)
        # self.seq_num = self.seq_num + 1
        header: bytes = PacketHeader(msgtype, self.seq_num, length).to_bytes()
        self.sendto((header.decode() + " " + data.decode()).encode(), address)

    def recv(self) -> Tuple[bytes, Tuple[str, int]]:
        (data, address) = self.recvfrom()

        if data is None or address is None:
            return ("Drop".encode(), NO_ADDRESS)

        if PacketHeader(data=data).verify_packet():
            # Send ACK MSG automatically
            if PacketHeader(data=data).get_msg_type() != MSGType.ACK:
                self.send(MSGType.ACK, bytes(), address)

            if PacketHeader(data=data).get_msg_type() == MSGType.START:
                # print("Recieved Start MSG")
                return (data, address)

            if self.accepted:
                # print("Recieved Other MSG")
                return (data, address)

        return ("Drop".encode(), NO_ADDRESS)

    def close(self, address: Tuple[str, int]):
        self.send(MSGType.END, bytes(), address)
