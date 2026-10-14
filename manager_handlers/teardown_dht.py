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
    manager_info.dht_ring_size = -1
    manager_info.has_dht_exist = False
    manager_info.peers_dht_table = []

    return "SUCCESS"


def has_invalid_teardown_dht(args):
    try:
        _ = args[0]
    except:
        return True
    return False
