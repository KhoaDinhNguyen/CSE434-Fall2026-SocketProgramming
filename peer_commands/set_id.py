import peer_info


def do_set_id(args):
    ip = args[0]
    p_port = int(args[1])
    id = int(args[2])
    ring_size = int(args[3])
    r_name = args[4]
    r_ip = args[5]
    r_port = args[6]
    table_size = int(args[7])

    #
    p_addr = (ip, p_port)
    # Right neighbor
    # r_name = args[4]

    # Send data
    message = (
        f"set-id {ip} {p_port} {id} {ring_size} {r_name} {r_ip} {r_port} {table_size}"
    )
    peer_info.p_socket.sendto(message.encode("utf-8"), p_addr)

    print(f"[SEND] -> {p_addr}: {message}")


def handle_set_id(args, peer_address):
    params = args.split(" ")
    ip = params[0]
    p_port = int(params[1])
    id = int(params[2])
    ring_size = int(params[3])
    r_name = params[4]
    r_ip = params[5]
    r_port = int(params[6])
    table_size = int(params[7])

    peer_info.id = id
    peer_info.ring_size = ring_size
    peer_info.r_name = r_name
    peer_info.r_ip = r_ip
    peer_info.r_port = r_port
    peer_info.hash_table_size = table_size
    peer_info.local_hash_table = peer_info.LocalHashTable(table_size)

    message = f"Has set id={id} ring_size={ring_size} r_neighbour=({r_name}, {r_ip}, {r_port})"

    print(f"[SEND] -> {peer_address}: SUCCESS")

    peer_info.p_socket.sendto(message.encode("utf-8"), peer_address)
