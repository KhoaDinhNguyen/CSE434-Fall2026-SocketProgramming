import manager_info
import random


def handle_setup_dht(args) -> str:
    leader_name = args[0]
    nusers = int(args[1])
    year = int(args[2])

    print(args)
    print(manager_info.peers_network[leader_name])
    # Assign peer name to be leader name
    manager_info.peers_network[leader_name].state = "LEADER"

    free_peers = [
        peer.name
        for peer in manager_info.peers_network.values()
        if peer.state == "FREE" and peer.name != leader_name
    ]

    # Set random seed to recreate the result
    random.seed(42)

    # Random select n - 1 peer
    indth_peer_names = random.sample(free_peers, nusers - 1)

    # Manage peer_dht_table
    for peer_name in indth_peer_names:
        manager_info.peers_network[peer_name].state = "INDHT"

    manager_info.peers_dht_table.append(leader_name)
    manager_info.peers_dht_table.extend(indth_peer_names)

    return (
        "SUCCESS\n"
        + manager_info.output_peers_dht_table()
        + "\n"
        + manager_info.output_leader_task()
    )
