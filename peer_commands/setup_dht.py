import peer_info


def do_setup_dht(params, manager_addr):
    leader_name = params[0]
    nusers = int(params[1])
    year = int(params[2])

    if leader_name != peer_info.name:
        return

    # Send to manager
    message = f"setup-dht {leader_name} {nusers} {year}"
    print(f"[SEND] -> {manager_addr}: {message}")
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    # Receive data
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")
