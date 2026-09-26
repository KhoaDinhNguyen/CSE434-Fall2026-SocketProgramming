import manager_info
import random
from pathlib import Path


def handle_setup_dht(args) -> str:
    if has_invalid_setup_dht_args(args):
        return "FAILURE"

    leader_name = args[0]
    ring_size = int(args[1])
    year = int(args[2])

    manager_info.has_dht_exist = True

    # Update DHT information

    # Leader name
    manager_info.dht_leader_name = leader_name
    manager_info.dht_ring_size = ring_size
    manager_info.dht_year = year
    manager_info.peers_network[leader_name].state = "LEADER"

    # Random select n - 1 peer
    indth_peer_names = random_select_free_users(ring_size - 1)

    # Update free users to INDHT
    for peer_name in indth_peer_names:
        manager_info.peers_network[peer_name].state = "INDHT"

    # Insert peer_name in ring topology in order
    manager_info.peers_dht_table.append(leader_name)
    manager_info.peers_dht_table.extend(indth_peer_names)

    # Waits dht-complete from leader
    manager_info.is_waiting_dht_complete = True

    print("Waiting for dht-complete from leader...")

    return manager_info.output_peers_dht_table()


def has_invalid_setup_dht_args(args) -> bool:
    try:
        leader_name = args[0]
        ring_size = int(args[1])
        year = int(args[2])

        # Failures when
        #   - DHT already exists
        #   - leader_name is not registered
        #   - ring size less than 3 or greater than numbers of registered users
        #   - year file must exist
        if manager_info.has_dht_exist:
            return True
        elif leader_name not in manager_info.peers_network:
            return True
        elif ring_size < 3 or ring_size > len(manager_info.peers_network):
            return True
        # elif Path.exists(f"details-{year}.csv.gz"):
        #     return True
    except:
        return True

    return False


def random_select_free_users(n_size: int):
    free_peers = [
        peer.name
        for peer in manager_info.peers_network.values()
        if peer.state == "FREE"
    ]

    random.seed(42)

    return random.sample(free_peers, n_size)
