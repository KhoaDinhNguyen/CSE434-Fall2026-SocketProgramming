import peer_info


def do_leave_dht(args, manager_addr):
    if has_invalid_do_leave_dht(args):
        print("Invalid request")
        return

    peer_name = args[0]

    # Send command
    message = f"leave-dht {peer_name}"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> {manager_addr}: leave-dht {peer_name}")

    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")


def has_invalid_do_leave_dht(args) -> bool:
    return not isinstance(args, list) or len(args) < 1
