import peer_info
import time


def do_reset_id(args):
    if has_invalid_do_reset_id(args):
        print("Invaid request")
        return

    init_peer_name = args[0]
    id = int(args[1])
    ring_size = int(args[2])
    is_leave = args[3]

    forward_reset_id(
        [
            init_peer_name,
            id,
            ring_size,
            peer_info.r_name,
            peer_info.r_ip,
            peer_info.r_port,
            is_leave,
        ]
    )


def forward_reset_id(args):
    if has_invalid_do_reset_id(args):
        print("Invaid request")
        return

    init_peer_name = args[0]
    id = int(args[1])
    ring_size = int(args[2])
    r_name = args[3]
    r_ip = args[4]
    r_port = args[5]
    is_leave = args[6]

    r_neighbor_addr = (peer_info.r_ip, peer_info.r_port)

    message = f"reset-id {init_peer_name} {id} {ring_size} {r_name} {r_ip} {r_port} {is_leave}"
    peer_info.p_socket.sendto(message.encode("utf-8"), r_neighbor_addr)

    print(f"[SEND] -> {r_neighbor_addr}: {message}")


def handle_reset_id(args, peer_addr):
    init_peer_name = args[0]
    id = int(args[1])
    ring_size = int(args[2])
    r_name = args[3]
    r_ip = args[4]
    r_port = args[5]
    is_leave = args[6]

    peer_info.id = id
    peer_info.ring_size = ring_size

    print(f"Reset id {peer_info.id}")

    # Acknowledge
    message = "SUCCESS"

    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)
    print(f"[SEND] -> {peer_addr}: {message}")

    if init_peer_name != peer_info.name:
        time.sleep(2)
        print("Send reset-id to the next neighbor")
        forward_reset_id(
            [init_peer_name, id + 1, ring_size, r_name, r_ip, r_port, is_leave]
        )
    elif init_peer_name == peer_info.r_name and is_leave == "true":
        peer_info.r_name = r_name
        peer_info.r_ip = r_ip
        peer_info.r_port = r_port
    else:
        print("Last node in the cycle detected. Do nothing")

    print(f"I'm {peer_info.name}, my neighbor is {peer_info.r_name}")


def has_invalid_do_reset_id(args):
    try:
        init_peer_name = args[0]
        id = int(args[1])
        ring_size = int(args[2])
        is_leave = args[3]
    except:
        return True

    return False
