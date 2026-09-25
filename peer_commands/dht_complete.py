import peer_info


def do_dht_complete(manager_addr):
    message = "dht-complete"

    # send data
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)
    print(f"[SEND] -> {manager_addr}: {message}")
    # receive data

    reponse, _ = peer_info.m_socket.recvfrom(4096)
    reponse = reponse.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {reponse}")
