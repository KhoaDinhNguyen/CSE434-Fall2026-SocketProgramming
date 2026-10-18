import random
import manager_info


def handle_query_dht(args) -> str:
    if has_invalid_query_dht_args(args):
        return "FAILURE"

    # Randomly choose one peer that is currently part of the DHT
    selected_name = random.choice(manager_info.peers_dht_table)
    selected_peer = manager_info.peers_network[selected_name]

    # Return SUCCESS as well as the selected peer's 3-tuple
    return (
        f"SUCCESS {selected_peer.name} "
        f"{selected_peer.ip} {selected_peer.p_port}"
    )


def has_invalid_query_dht_args(args) -> bool:
    # query-dht command should have exactly one argument: peer-name
    if len(args) != 1:
        return True

    peer_name = args[0]

    # Requesting peer must be registered
    if peer_name not in manager_info.peers_network:
        return True

    # A DHT must exist
    if not manager_info.has_dht_exist:
        return True

    # DHT setup must be finished
    if manager_info.is_waiting_dht_complete:
        return True

    # Only a FREE peer can query the DHT
    if manager_info.peers_network[peer_name].state != "FREE":
        return True

    # There must actually be DHT peers available
    if len(manager_info.peers_dht_table) == 0:
        return True

    return False