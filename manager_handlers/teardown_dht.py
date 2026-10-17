import manager_info


def handle_teardown_dht(args):
    if has_invalid_teardown_dht(args):
        return "FAILURE"

    peer_name = args[0]

    if peer_name != manager_info.dht_leader_name:
        return "FAILURE"

    manager_info.is_waiting_teardown_complete = True

    print("Waiting for teardown-complete from the manager...")
    return "SUCCESS"


def handle_teardown_complete(args):
    if has_invalid_teardown_dht(args):
        return "FAILURE"

    peer_name = args[0]

    if peer_name != manager_info.dht_leader_name:
        return "FAILURE"

    for peer_name in manager_info.peers_network.keys():
        manager_info.peers_network[peer_name].state = "FREE"

    manager_info.is_waiting_teardown_complete = False
    manager_info.dht_leader_name = ""
    manager_info.dht_ring_size = 0
    manager_info.dht_year = 0
    manager_info.has_dht_exist = False
    manager_info.peers_dht_table = []

    return "SUCCESS"


def has_invalid_teardown_dht(args) -> bool:
    return not isinstance(args, list) or len(args) < 1
