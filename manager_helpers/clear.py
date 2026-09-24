from . import peers, dht
from command_status import success_code


def clear():

    dht.dhtInstance = None
    peers.peers_network = {}

    print("[SUCCESS]: Clear all states")

    return success_code
