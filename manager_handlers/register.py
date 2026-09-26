import manager_info
from manager_info import Peer


def handle_register(args) -> str:
    if has_invalid_register_args(args):
        return "FAILURE"

    # Retrieves information
    name = args[0]
    ip = args[1]
    m_port = int(args[2])
    p_port = int(args[3])

    # Stores ports in manager information
    manager_info.peers_network[name] = Peer(name, ip, m_port, p_port)

    # Puts used ports into set for later checking
    manager_info.used_ports.add(m_port)
    manager_info.used_ports.add(p_port)

    return "SUCCESS"


def has_invalid_register_args(args) -> bool:
    try:
        name = args[0]
        ip = args[1]
        m_port = int(args[2])
        p_port = int(args[3])

        if name in manager_info.peers_network or len(name) > 15:
            return True

        if m_port in manager_info.used_ports or p_port in manager_info.used_ports:
            return True
    except:
        return True

    return False
