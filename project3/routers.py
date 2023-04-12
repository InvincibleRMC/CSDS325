from client import Client
from constants import STARTING_CONFIG
import signal
from typing import List
from threading import Thread
import time


ANSWER = [Client("u", {"x": 5, "w": 3, "v": 6, "y": 10, "z": 12, "u": 0}),
          Client("x", {"x": 0, "w": 4, "v": 7, "y": 7, "z": 9, "u": 5}),
          Client("w", {"x": 4, "w": 0, "v": 3, "y": 7, "z": 9, "u": 3}),
          Client("v", {"x": 7, "w": 3, "v": 0, "y": 4, "z": 6, "u": 6}),
          Client("y", {"x": 7, "w": 7, "v": 4, "y": 0, "z": 2, "u": 10}),
          Client("z", {"x": 9, "w": 9, "v": 6, "y": 2, "z": 0, "u": 12})]

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    client_list: List[Client] = []

    for key in STARTING_CONFIG:
        client = Client(key)
        Thread(target=client.main).start()
        client_list.append(client)

    time.sleep(5)

    print("\nDone")
    for client in client_list:
        print(client)
    print("")

    print("ANSWER")
    for client in ANSWER:
        print(client)
