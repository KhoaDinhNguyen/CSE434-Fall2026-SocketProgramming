import peer_info


def do_set_id(args, peer_addr):
    if has_invalid_set_id_args(args):
        print("Invalid request")
        return

    id = int(args[0])
    ring_size = int(args[1])
    r_name = args[2]
    r_ip = args[3]
    r_port = args[4]
    table_size = int(args[5])

    # Sends set-id to other peers
    message = f"set-id {id} {ring_size} {r_name} {r_ip} {r_port} {table_size}"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def handle_set_id(args, peer_addr):
    id = int(args[0])
    ring_size = int(args[1])
    r_name = args[2]
    r_ip = args[3]
    r_port = int(args[4])
    table_size = int(args[5])

    peer_info.id = id
    peer_info.ring_size = ring_size
    peer_info.r_name = r_name
    peer_info.r_ip = r_ip
    peer_info.r_port = r_port
    peer_info.hash_table_size = table_size
    peer_info.local_hash_table = peer_info.LocalHashTable(table_size)

    # Acknowledge the setup
    message = f"At {peer_addr}, it has set id={id} ring_size={ring_size} r_neighbour=({r_name}, {r_ip}, {r_port})"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: SUCCESS")


def has_invalid_set_id_args(args):
    try:
        id = int(args[0])
        ring_size = int(args[1])
        r_name = args[2]
        r_ip = args[3]
        r_port = args[4]
        table_size = int(args[5])
    except:
        return True

    return False
