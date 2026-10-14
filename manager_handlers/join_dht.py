from manager_handlers.setup_dht import random_select_in_dht_users
import manager_info


def handle_join_dht(args):
    if has_invalid_join_dht_args(args):
        return "FAILURE"

    peer_name = args[0]
    manager_info.requester_name = peer_name
    manager_info.is_waiting_dht_rebuilt = True
    manager_info.requester_command = "join-dht"

    print("Waiting for dht-rebult from same peer name...")

    return handle_random_peer()


def has_invalid_join_dht_args(args):
    try:
        peer_name = args[0]

        if manager_info.peers_network[peer_name].state != "FREE":
            return True
    except:
        return True

    return False


def handle_random_peer():
    random_peer_name = random_select_in_dht_users(n_size=1)[0]

    name = manager_info.peers_network[random_peer_name].name
    ip = manager_info.peers_network[random_peer_name].ip
    p_port = manager_info.peers_network[random_peer_name].p_port

    response = f"{name} {ip} {p_port}"

    return response
