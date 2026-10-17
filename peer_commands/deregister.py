import peer_info

def do_deregister(args, manager_addr):
    if has_invalid_deregister_args(args):
        print("Invalid request")
        return False

    peer_name = args[0]

    #Send deregister request to manager
    message = f"deregister {peer_name}"
    peer_info.m_socket.sendto(
        message.encode("utf-8"),
        manager_addr
    )

    print(f"[SEND] -> {manager_addr}: {message}")

    # Receive response from manager
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")

    if response == "SUCCESS":
        return True

    return False


def has_invalid_deregister_args(args):
    try:
        peer_name = args[0]

        # Peer must already be registered
        if peer_info.name is None:
            return True

        # A peer should only deregister itself
        if peer_name != peer_info.name:
            return True

    except:
        return True

    return False