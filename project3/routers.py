from client import Client
import threading
from constants import STARTING_CONFIG
import signal
import time
from typing import List
from multiprocessing import Process

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    client_list: List[Client] = []

    # count = 16000

    for keys in STARTING_CONFIG:
        client = Client(["JUNK", keys])
        # threading.Thread(target=client.main,).start()
        Process(target=client.main,).start()
        # p.start()
        # p.join()

        client_list.append(client)
        # count = count + 1

    time.sleep(5)

    print("Done")
    for client in client_list:
        print(f'Client {client.name} has DV = {client.dv}')
