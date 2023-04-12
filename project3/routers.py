from client import Client, ClientManager
from constants import STARTING_CONFIG
import signal
import time
from typing import List
from multiprocessing import Process


ANSWER = [Client("u", {"x": 5, "w": 3, "v": 6, "y": 10, "z": 12, "u": 0})]

if __name__ == "__main__":
    ClientManager.register('Client', Client)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    client_list: List[Client] = []
    p_list: List[Process] = []

    # counter: int = 23000

    with ClientManager() as m:
        for keys in STARTING_CONFIG:
            client: Client = m.Client(keys)
            p = Process(target=client.main)
            p.start()
            p_list.append(p)
            client_list.append(client)
            # counter = counter + 1

        time.sleep(30)

        print("\nDone")
        for client in client_list:
            print(client.__str__())
        print("")

        for p in p_list:
            p.terminate()

        for client in ANSWER:
            print(client)
