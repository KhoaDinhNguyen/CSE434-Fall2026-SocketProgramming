import peer_info
from utils import create_udp_socket


def do_register(args, manager_addr):
    if peer_info.name is not None or has_invalid_register_args(args):
        print("Invalid request")
        return

    name = args[0]
    ip = args[1]
    m_port = int(args[2])
    p_port = int(args[3])

    # Create sockets
    peer_info.m_socket = create_udp_socket(m_port)
    peer_info.p_socket = create_udp_socket(p_port)

    # Ask manager to create a slot in peer networks
    message = f"register {name} {ip} {m_port} {p_port}"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> Manager {manager_addr}: {message}")

    # Receive data from manager
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- Manager {manager_addr}: {response}")

    # Set up permanent values for process
    if response == "SUCCESS":
        peer_info.name = name
        peer_info.state = "FREE"
    else:
        peer_info.m_socket.close()
        peer_info.p_socket.close()
        peer_info.m_socket = None
        peer_info.p_socket = None


def has_invalid_register_args(args):
    try:
        name = args[0]
        ip = args[1]
        m_port = int(args[2])
        p_port = int(args[3])
    except:
        return True

    return False
