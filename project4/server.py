import socket
import signal
import sys

HTTP_PORT = 80

# Kills with Control + C
signal.signal(signal.SIGINT, signal.SIG_DFL)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

args = sys.argv
if len(args) != 3:
    raise Exception("Missing Arguments")

client_sock.bind((args[1], int(args[2])))
client_sock.listen(1)
conn, addr = client_sock.accept()
while True:
    data = conn.recv(4096)
    if not data:
        break

    link = data.decode().replace("http://", "")

    split = link.split("/", 1)

    name = split[0].replace("GET ", "")

    path = (split[1].split(" ", 1))[0]

    http_sock.connect((name, HTTP_PORT))

    GET = f"GET /{path} HTTP/1.1\r\nHost:{name}\r\nConnection: close\r\n\r\n".encode()

    print("Send Request from Proxy")
    http_sock.send(GET)
    while True:
        reply = http_sock.recv(4096)
        if reply:
            break

    print(reply.decode())

    conn.sendall(reply)
    http_sock.close()

conn.close()
