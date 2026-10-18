from manager_handlers.setup_dht import random_select_in_dht_users
import manager_info


def handle_join_dht(args):
    if has_invalid_join_dht_args(args):
        return "FAILURE"

    peer_name = args[0]

    if manager_info.peers_network[peer_name].state != "FREE" or not manager_info.has_dht_exist:
        return "FAILURE"

    manager_info.requester_name = peer_name
    manager_info.is_waiting_dht_rebuilt = True
    manager_info.requester_command = "join-dht"

    print("Waiting for dht-rebult from same peer name...")

    return handle_random_peer()


def has_invalid_join_dht_args(args) -> bool:
    return not isinstance(args, list) or len(args) < 1


def handle_random_peer():
    random_peer_name = random_select_in_dht_users(n_size=1)[0]
    peer = manager_info.peers_network[random_peer_name]

    response = f"{peer.name} {peer.ip} {peer.p_port}"
    return response
