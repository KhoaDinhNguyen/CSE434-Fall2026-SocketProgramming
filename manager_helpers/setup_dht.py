from command_status import failure_code, success_code
from . import peers
from . import dht
import random


def setup_dht(*args):
    params = args[0]

    try:
        leader_name = params[0]
        num_users = int(params[1])
        year = int(params[2])
    except:
        return failure_code

    if dht.dhtInstance != None:
        return failure_code
    if leader_name not in peers.peers_network:
        return failure_code
    if num_users < 3 or num_users > len(peers.peers_network):
        return failure_code

    dht.dhtInstance = dht.DHT(leader_name, num_users, year)

    # Set leader name status
    peers.peers_network[leader_name].state = peers.PeerState.LEADER
    dht.dhtInstance.peers_in_dht.append(leader_name)

    # Random select n - 1 peer
    free_peers = [
        peer.peer_name
        for peer in peers.peers_network.values()
        if peer.state == peers.PeerState.FREE
    ]

    # Set random seed to recreate the result
    random.seed(42)

    chosen_peer_names = random.sample(free_peers, num_users - 1)

    for name in chosen_peer_names:
        peers.peers_network[name].state = peers.PeerState.INDHT
        dht.dhtInstance.peers_in_dht.append(name)

    print(f"[SETUP DHT] Success. Waiting for leader's tasks")

    return success_code
