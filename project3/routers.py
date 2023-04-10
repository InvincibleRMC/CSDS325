from client import Client
import threading
from constants import STARTING_CONFIG
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)
for keys in STARTING_CONFIG:
    t = threading.Thread(target=Client(["JUNK", keys]).main).start()
