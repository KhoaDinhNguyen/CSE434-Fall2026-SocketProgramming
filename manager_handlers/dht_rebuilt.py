import manager_info


def handle_dht_rebuilt(args):
    if has_invalid_handle_dht_rebuilt_args(args):
        return "FAILURE"

    peer_name, leader_name = args[0], args[1]

    # Only requester can call dht-rebuilt
    if peer_name != manager_info.requester_name:
        return "FAILURE"

    if manager_info.requester_command == "leave-dht":
        manager_info.peers_network[manager_info.dht_leader_name].state = "INDHT"
        manager_info.peers_network[leader_name].state = "LEADER"
        manager_info.peers_network[peer_name].state = "FREE"
        manager_info.dht_leader_name = leader_name
        manager_info.dht_ring_size = manager_info.dht_ring_size - 1

        # Update the dht_table
        manager_info.peers_dht_table.remove(peer_name)
    else:
        manager_info.peers_network[manager_info.dht_leader_name].state = "INDHT"
        manager_info.peers_network[leader_name].state = "LEADER"
        manager_info.peers_network[peer_name].state = "INDHT"
        manager_info.dht_leader_name = leader_name
        manager_info.dht_ring_size = manager_info.dht_ring_size + 1

        # Update the dht_table
        new_peers_dht_table = []
        for peer_name in manager_info.peers_dht_table:
            if peer_name == leader_name:
                new_peers_dht_table.append(manager_info.requester_name)
            new_peers_dht_table.append(peer_name)
        manager_info.peers_dht_table = new_peers_dht_table

    return "SUCCESS"


def has_invalid_handle_dht_rebuilt_args(args: list) -> bool:
    return not isinstance(args, list) or len(args) < 2
