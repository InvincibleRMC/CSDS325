import socket
import signal
import sys
from typing import List

GREETING: str = "GREETING"
MESSAGE: str = "MESSAGE"
INCOMING: str = "INCOMING"


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def send_init_message(self):
        message: str = GREETING + " " + self.udp_ip + " " + self.udp_port
        self.s.sendto(message.encode(), (self.udp_ip, self.udp_port))


    def main(self, args: List[str]):
        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.udp_ip = args[1]
        self.udp_port = args[2]
        # MESSAGE = b"MESSAGE HI BESTIE"
        # s.sendto(MESSAGE, (udp_ip, udp_port))
        data = s.recv(1024)
        s.close()
        print('Received', repr(data))


    main(sys.argv)
