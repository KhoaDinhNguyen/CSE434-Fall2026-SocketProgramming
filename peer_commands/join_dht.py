import peer_info


def do_join_dht(args, manager_addr):
    if has_invalid_do_join_dht(args):
        print("Invalid request")
        return

    peer_name = args[0]
    message = f"join-dht {peer_name}"

    # Send command
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)
    print(f"[SEND] -> {manager_addr}: join-dht {peer_name}")

    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")


def do_random_peer(manager_addr):
    # Send command
    message = "random-peer"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> {manager_addr}: {message}")

    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")


def do_update_right_neighbor(args):
    peer_ip = args[0]
    peer_port = int(args[1])
    name = args[2]  # new peer name
    ip = args[3]  # new peer ip
    port = int(args[4])  # new peer port

    peer_addr = (peer_ip, peer_port)

    message = f"update-right-neighbor {name} {ip} {port}"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def handle_update_right_neighbor(args, peer_addr):
    name = args[0]
    ip = args[1]
    port = int(args[2])

    # Old state
    r_name = peer_info.r_name
    r_ip = peer_info.r_ip
    r_port = peer_info.r_port
    hash_table_size = peer_info.hash_table_size
    ring_size = peer_info.ring_size
    year = peer_info.year

    # New state
    peer_info.r_name = name
    peer_info.r_ip = ip
    peer_info.r_port = port

    print(f"Successfully reassign neighbor to be {name} ({ip}, {port})")

    message = f"set-right-neighbor {r_name} {r_ip} {r_port} {hash_table_size} {ring_size} {year}"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def handle_set_right_neighbor(args, peer_addr):
    r_name = args[0]
    r_ip = args[1]
    r_port = int(args[2])
    hash_table_size = int(args[3])
    ring_size = int(args[4])
    year = int(args[5])

    peer_info.r_name = r_name
    peer_info.r_ip = r_ip
    peer_info.r_port = r_port
    peer_info.hash_table_size = hash_table_size
    peer_info.ring_size = ring_size
    peer_info.year = year
    peer_info.local_hash_table = peer_info.LocalHashTable(hash_table_size)

    print(f"Successfully reassign neighbor to be {r_name} ({r_ip}, {r_port})")

    message = f"SUCCESS"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def has_invalid_do_join_dht(args) -> bool:
    return not isinstance(args, list) or len(args) < 1
