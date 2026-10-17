import peer_info


def do_set_id(args, peer_addr):
    if has_invalid_set_id_args(args):
        print("Invalid request")
        return

    id = int(args[0])
    ring_size = int(args[1])
    year = int(args[2])
    r_name = args[3]
    r_ip = args[4]
    r_port = args[5]
    table_size = int(args[6])
    dht_peer_args = args[7:]
    peer_table = " ".join(str(value) for value in dht_peer_args)

    # Sends set-id to other peers
    message = f"set-id {id} {ring_size} {year} {r_name} {r_ip} {r_port} {table_size} {peer_table}"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def handle_set_id(args, peer_addr):
    id = int(args[0])
    ring_size = int(args[1])
    year = int(args[2])
    r_name = args[3]
    r_ip = args[4]
    r_port = int(args[5])
    table_size = int(args[6])
    dht_peer_args = args[7:]

    peer_info.id = id
    peer_info.ring_size = ring_size
    peer_info.year = year
    peer_info.r_name = r_name
    peer_info.r_ip = r_ip
    peer_info.r_port = r_port
    peer_info.hash_table_size = table_size
    peer_info.local_hash_table = peer_info.LocalHashTable(table_size)

    # Save all DHT peers by node ID
    peer_info.dht_peers = {}
    for peer_id in range(ring_size):
        start = peer_id * 3
        name = dht_peer_args[start]
        ip = dht_peer_args[start + 1]
        p_port = int(dht_peer_args[start + 2])
        peer_info.dht_peers[peer_id] = (name, ip, p_port)
    # Acknowledge the setup
    message = "SUCCESS"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def has_invalid_set_id_args(args):
    try:
        id = int(args[0])
        ring_size = int(args[1])
        year = int(args[2])
        r_name = args[3]
        r_ip = args[4]
        r_port = args[5]
        table_size = int(args[6])
        dht_peer_args = args[7:]
    except:
        return True

    return False
