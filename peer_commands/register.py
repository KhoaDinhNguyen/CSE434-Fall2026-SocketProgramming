import peer_info
from utils import create_udp_socket


def do_register(params, manager_addr):

    if peer_info.name is not None:
        return

    name = params[0]
    ip = params[1]
    m_port = int(params[2])
    p_port = int(params[3])

    # Create sockets
    peer_info.m_socket = create_udp_socket(m_port)
    peer_info.p_socket = create_udp_socket(p_port)

    # Ask manager to create a slot in peer networks
    message = f"register {name} {ip} {m_port} {p_port}"
    print(f"[SEND] -> Manager {manager_addr}: {message}")

    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    # Receive data from manager
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- Manager {manager_addr}: {response}")

    # Set up permanent values for process
    if response == "SUCCESS":
        peer_info.name = name
        peer_info.state = "FREE"
    else:
        print("Register failed")
        peer_info.m_socket.close()
        peer_info.p_socket.close()
        peer_info.m_socket = None
        peer_info.p_socket = None
