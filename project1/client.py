import socket
import signal
import sys
from typing import List
from threading import Thread

GREETING: str = "GREETING"
MESSAGE: str = "MESSAGE"
INCOMING: str = "INCOMING"
TIMEOUT: int = 2


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_init_message(self):
        message: str = GREETING + " " + self.udp_ip + " " + str(self.udp_port)
        self.s.sendto(message.encode(), (self.udp_ip, self.udp_port))

    def send_message(self):
        while True:
            msg: str = MESSAGE + " " + input()
            self.s.sendto(msg.encode(), (self.udp_ip, self.udp_port))

    def recieve_incoming(self):
        while True:
            data = self.s.recv(1024)
            json = data.decode()
            message_type = json.split(" ")[0]
            message_contents = json.split(" ", 1)[1]
            if message_type == INCOMING:
                print(message_contents)
            else:
                print("Invalid Server Message")

    def main(self, args: List[str]):
        # Kills with Control + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.udp_ip: str = args[1]
        self.udp_port: int = int(args[2])

        self.send_init_message()

        t1 = Thread(target=self.send_message)
        t2 = Thread(target=self.recieve_incoming)

        t1.start()
        t2.start()

        t1.join()
        t2.join()


Client().main(sys.argv)
