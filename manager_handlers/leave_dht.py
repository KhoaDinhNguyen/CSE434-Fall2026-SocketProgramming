import manager_info


def handle_leave_dht(args):
    if has_invalid_leave_dht_args(args):
        return "FAILURE"

    peer_name = args[0]
    manager_info.requester_name = peer_name
    manager_info.is_waiting_dht_rebuilt = True
    manager_info.requester_command = "leave-dht"

    print("Waiting for dht-rebult from same peer name...")

    return "SUCCESS"


def has_invalid_leave_dht_args(args):
    try:
        peer_name = args[0]

        if manager_info.peers_network[peer_name].state == "FREE":
            return True
    except:
        return True

    return False
