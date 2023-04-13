from dataclasses import dataclass
from typing import List

PORT = 5555
ADDRESS = "localhost"

PORT_ADDRESS = (ADDRESS, PORT)

JOIN: str = "JOIN"
UPDATE: str = "UPDATE"
INCOMING: str = "INCOMING"


@dataclass
class Pairs:
    Node: str
    cost: int


# STARTING_CONFIG = {"x": [Pairs("y", 1), Pairs("z", 5)],
#                    "y": [Pairs("x", 1), Pairs("z", 2)],
#                    "z": [Pairs("x", 5), Pairs("y", 2)]}


STARTING_CONFIG = {"u": [Pairs("x", 5), Pairs("w", 3), Pairs("v", 7), Pairs("y", -1), Pairs("z", -1), Pairs("u", 0)],
                   "x": [Pairs("x", 0), Pairs("w", 4), Pairs("v", -1), Pairs("y", 7), Pairs("z", 9), Pairs("u", 5)],
                   "w": [Pairs("x", 4), Pairs("w", 0), Pairs("v", 3), Pairs("y", 8), Pairs("z", -1), Pairs("u", 3)],
                   "v": [Pairs("x", -1), Pairs("w", 3), Pairs("v", 0), Pairs("y", 4), Pairs("z", -1), Pairs("u", 7)],
                   "y": [Pairs("x", 7), Pairs("w", 8), Pairs("v", 4), Pairs("y", 0), Pairs("z", 2), Pairs("u", -1)],
                   "z": [Pairs("x", 9), Pairs("w", -1), Pairs("v", -1), Pairs("y", 2), Pairs("z", 0), Pairs("u", -1)]}


def str_to_pair_list(message_contents: str) -> List[Pairs]:
    """Helper to parse the message back into a list"""
    clean = message_contents.replace("[", "")
    clean = clean.replace("]", "")
    clean = clean.replace("Pairs(Node='", "")
    clean = clean.replace("'", "")
    clean = clean.replace("cost=", "")
    clean = clean.replace(")", "")
    clean = clean.replace(" ", "")

    splitted = clean.split(",")
    counter = 0
    pair_list: List[Pairs] = []
    while counter < len(splitted):
        node = splitted[counter]
        cost = int(splitted[counter + 1])
        pair_list.append(Pairs(node, cost))
        counter = counter + 2
    return pair_list
