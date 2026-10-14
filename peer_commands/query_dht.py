import peer_info

def do_query_dht(args, manager_addr):
    if has_invalid_query_dht_args(args):
        print("Invalid request")
        return

    peer_name = args[0]
    event_id = args[1]

    # Ask manager for a random peer in the DHT
    message = f"query-dht {peer_name}"

    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)
    print(f"[SEND] -> {manager_addr}: {message}")

    # Receive manager response
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8").strip()

    print(f"[RECV] <- {manager_addr}: {response}")

    if response == "FAILURE":
        return

    # Expected:
    # SUCCESS <peer-name> <ip> <p-port>
    params = response.split(" ")

    selected_name = params[1]
    selected_ip = params[2]
    selected_port = int(params[3])

    selected_addr = (selected_ip, selected_port)

    # Begin the actual DHT search
    message = (
        f"find-event {event_id} "
        f"{peer_info.name} {peer_info.ip} {peer_info.p_port}"
    )

    peer_info.p_socket.sendto(message.encode("utf-8"), selected_addr)

    print(f"[SEND] -> {selected_name} {selected_addr}: {message}")


def has_invalid_query_dht_args(args):
    try:
        peer_name = args[0]
        event_id = int(args[1])
    except:
        return True

    return False