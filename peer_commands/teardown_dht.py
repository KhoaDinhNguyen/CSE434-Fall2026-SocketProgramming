import peer_info
import time


def do_teardown(args):
    if has_invalid_do_teardown(args):
        print("Invalid request")
        return

    init_peer_name = args[0]
    r_neighbor_addr = (peer_info.r_ip, peer_info.r_port)

    message = f"teardown {init_peer_name}"
    peer_info.p_socket.sendto(message.encode("utf-8"), r_neighbor_addr)

    print(f"[SEND] -> {r_neighbor_addr}: {message}")


def handle_teardown(args, peer_addr):
    init_peer_name = args[0]

    peer_info.local_hash_table.clear()

    print("Successfully clear local hash table")

    message = "SUCCESS"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")

    if init_peer_name != peer_info.name:
        time.sleep(2)
        print("Propagate teardown to the right neighbor")
        do_teardown([init_peer_name])


def do_teardown_dht(args, manager_addr):
    if has_invalid_do_teardown(args):
        print("Invalid request")
        return

    leader_name = args[0]

    # Send command
    message = f"teardown-dht {leader_name}"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> {manager_addr}: {message}")

    # Receive response
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")


def do_teardown_complete(args, manager_addr):
    if has_invalid_do_teardown(args):
        print("Invalid request")
        return

    leader_name = args[0]

    # Second command
    message = f"teardown-complete {leader_name}"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> {manager_addr}: {message}")

    # Receive response
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")


def has_invalid_do_teardown(args):
    return not isinstance(args, list) or len(args) < 1
