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
        print("Send teardown to the right neighbor")
        do_teardown([init_peer_name])


def has_invalid_do_teardown(args):
    try:
        init_peer_name = args[0]
    except:
        return True

    return False
