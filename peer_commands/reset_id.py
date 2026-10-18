import peer_info
import time


def do_reset_id(args):
    if has_invalid_do_reset_id(args):
        print("Invaid request")
        return

    init_peer_name = args[0]
    id = int(args[1])
    ring_size = int(args[2])

    forward_reset_id(
        [
            init_peer_name,
            peer_info.ip,
            peer_info.p_port,
            id,
            ring_size,
            peer_info.r_name,
            peer_info.r_ip,
            peer_info.r_port,
        ]
    )


def forward_reset_id(args):
    init_peer_name = args[0]
    init_peer_ip = args[1]
    init_peer_port = int(args[2])
    id = int(args[3])
    ring_size = int(args[4])
    leader_name = args[5]
    leader_ip = args[6]
    leader_port = int(args[7])

    r_neighbor_addr = (peer_info.r_ip, peer_info.r_port)

    # Send command
    message = f"reset-id {init_peer_name} {init_peer_ip} {init_peer_port} {id} {ring_size} {leader_name} {leader_ip} {leader_port}"
    peer_info.p_socket.sendto(message.encode("utf-8"), r_neighbor_addr)

    print(f"[SEND] -> {r_neighbor_addr}: {message}")


def handle_reset_id(args, peer_addr):
    init_peer_name = args[0]
    init_peer_ip = args[1]
    init_peer_port = int(args[2])
    id = int(args[3])
    ring_size = int(args[4])
    leader_name = args[5]
    leader_ip = args[6]
    leader_port = int(args[7])

    is_leave = ring_size < peer_info.ring_size

    peer_info.id = id
    peer_info.ring_size = ring_size
    peer_info.reorder_dht_peers(
        leader_name, is_leave, init_peer_name, init_peer_ip, init_peer_port
    )
    peer_info.print_dht_peers()

    print(f"Reset id to: {peer_info.id}")

    # Acknowledge
    message = "SUCCESS"

    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)
    print(f"[SEND] -> {peer_addr}: {message}")

    if init_peer_name != peer_info.name:
        time.sleep(2)
        print("Send reset-id to the next neighbor")
        forward_reset_id(
            [
                init_peer_name,
                init_peer_ip,
                init_peer_port,
                id + 1,
                ring_size,
                leader_name,
                leader_ip,
                leader_port,
            ]
        )
    else:
        print("Last node in the old cycle detected. Do nothing")

    if init_peer_name == peer_info.r_name and is_leave == True:
        peer_info.r_name = leader_name
        peer_info.r_ip = leader_ip
        peer_info.r_port = leader_port
        print(
            f"Last node in the new cycle detected in leave-dht, assign new right peer {leader_name} {leader_ip} {leader_port}"
        )


def has_invalid_do_reset_id(args) -> bool:
    return not isinstance(args, list) or len(args) < 3
