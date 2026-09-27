import peer_info


def do_dht_complete(args, manager_addr):
    if has_invalid_dht_complete_args(args):
        print("Invalid request")
        return

    peer_name = args[0]
    message = f"dht-complete {peer_name}"

    # Sends command
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)
    print(f"[SEND] -> {manager_addr}: {message}")

    # Receives response
    reponse, _ = peer_info.m_socket.recvfrom(4096)
    reponse = reponse.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {reponse}")


def has_invalid_dht_complete_args(args):
    try:
        peer_name = args[0]
    except:
        return True

    return False
