"""Server for CWRU Plan+"""
import socket
import sys
import time
import signal
from typing import List


def greeting():
    print("TODO")


def message():
    print("TODO")


def incoming():
    print("TODO")


UDI_IP = "localhost"
UDP_PORT = 50000


def main(args: List[str]):
    udp_port_num: int = int(args[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((UDI_IP, udp_port_num))

    # Kills with Control + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    while 1:
        data, addr = s.recvfrom(1024)
        json = data.decode()
        message_type = json.split(" ")[0]
        message_contents = json.split(" ", 1)[1]

        if message_type == "GREETING":
            greeting(message_contents)
        elif message_type == "MESSAGE":
            message(message_contents)
        elif message_type == "INCOMNIG":
            incoming(message_contents)
        else:
            print("Unkown message type ignoring message")

        print(data.decode)
        if not data:
            time.sleep(0.01)

    s.close()


main(sys.argv)
