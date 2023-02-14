"""Server for CWRU Plan+"""
import socket
import time
import signal

UDI_IP = "localhost"
UDP_PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDI_IP, UDP_PORT))


# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

while 1:
    data, addr = s.recvfrom(1024)
    print(data.decode)
    if not data:
        time.sleep(0.01)

s.close()
