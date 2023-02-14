import socket
import signal
import sys
from typing import List


def send_message():
    print("TODO")


def main(args: List[str]):
    # Kills with Control + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_ip = args[1]
    udp_port = args[2]
    MESSAGE = b"MESSAGE HI BESTIE"
    s.sendto(MESSAGE, (udp_ip, udp_port))
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))


main(sys.argv)
