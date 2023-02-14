import socket
import signal
# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDI_IP = "localhost"
UDP_PORT = 50000
MESSAGE = b"HI BESTIE"
s.sendto(MESSAGE, (UDI_IP, UDP_PORT))
data = s.recv(1024)
s.close()
print('Received', repr(data))
