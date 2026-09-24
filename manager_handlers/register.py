import manager_info
from manager_info import Peer


def handle_register(args) -> str:
    name = args[0]
    ip = args[1]
    m_port = int(args[2])
    p_port = int(args[3])

    print(args)

    if name in manager_info.peers_network:
        return "FAILURE"

    if m_port in manager_info.used_ports or p_port in manager_info.used_ports:
        return "FAILURE"

    manager_info.used_ports.add(m_port)
    manager_info.used_ports.add(p_port)

    manager_info.peers_network[name] = Peer(name, ip, m_port, p_port)

    return "SUCCESS"
