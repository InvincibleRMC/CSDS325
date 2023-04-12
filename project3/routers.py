from client import Client, ClientManager
from constants import STARTING_CONFIG
import signal
import time
from typing import List
from multiprocessing import Process

if __name__ == "__main__":
    ClientManager.register('Client', Client)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    client_list: List[Client] = []
    p_list: List[Process] = []

    with ClientManager() as m:
        for keys in STARTING_CONFIG:
            client: Client = m.Client(keys)
            p = Process(target=client.main,)
            p.start()
            p_list.append(p)
            client_list.append(client)

        time.sleep(5)

        print("\nDone")
        for client in client_list:
            print(f'Client {client.get_name()} has DV = {client.get_dv()}')
        print("")

        for p in p_list:
            p.terminate()
