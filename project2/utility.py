from enum import IntEnum
import socket
from typing import Tuple, Union, List
import threading
import time
import random
import zlib


class MSGType(IntEnum):
    ERROR = -1
    START = 0
    END = 1
    DATA = 2
    ACK = 3
    END_ACK = 4


class UnreliableSocket(socket.socket):

    def __init__(self):
        """Starts UnreliableSocket"""
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.settimeout(0.5)

    def bind(self, address: Tuple[str, int]):
        super().bind(address)

    def recvfrom(self):
        """Custom recvfrom with added package drop"""
        # Package Drop
        if random.random() < 0.15:
            return None, None
        # Needed for timeout
        try:
            data, addr = super().recvfrom(1472)
        except socket.timeout:
            return None, None

        # Data corruption
        if random.random() < 0.1:
            data = (data.decode()).split(" ", maxsplit=1)
            data = data[0] + " 15" + data[1]
            data = data.encode()

        return data, addr

    def sendto(self, data: bytes, address: Tuple[str, int]):
        # Duplicate Msg
        if random.random() < 0.1:
            super().sendto(data, address)
        # Delay Message
        if random.random() < 0.75:
            t1 = threading.Thread(target=lambda: time.sleep(0.1))
            t1.start()

        super().sendto(data, address)

    def close(self):
        super().close()


class PacketHeader():

    msg_type: MSGType  # 0: START; 1: END; 2: DATA; 3: ACK, 4: END_ACK
    seq_num: int  # Described below
    length: int  # Length of data; 0 for ACK, START and END packets
    checksum: int  # 32-bit CRC

    def __init__(self, msg_type: MSGType = MSGType.ERROR, seq_num: int = -1, length: int = -1, data: Union[bytes, None] = None):
        if data is not None:
            decode: List[str] = (data.decode()).split(" ")
            self.msg_type = MSGType(int(decode[0]))
            self.seq_num = int(decode[1])
            self.length = int(decode[2])
            self.checksum = int(decode[3])
        else:
            self.msg_type = msg_type
            self.seq_num = seq_num
            self.length = length
            self.checksum = self.compute_checksum()

    def compute_checksum(self) -> int:
        return zlib.crc32(str(self.msg_type + self.seq_num + self.length).encode())  # TA said we could use package for checksum

    def verify_packet(self):
        return self.compute_checksum() == self.checksum

    def to_bytes(self) -> bytes:
        return str(str(self.msg_type.numerator) + " " + str(self.seq_num) + " " + str(self.length) + " " + str(self.checksum)).encode()

    def decode(self) -> str:
        return self.to_bytes().decode()

    def get_msg_type(self) -> MSGType:
        return self.msg_type

    def get_seq_num(self) -> int:
        return self.seq_num
