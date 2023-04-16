import socket
import signal
import sys

# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

args = sys.argv
if len(args) != 4:
    raise Exception("Missing Args")

s.connect((args[1], int(args[2])))
s.sendall(args[3].encode())
data = s.recv(4096).decode()
s.close()
print(data)
