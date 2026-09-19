from .peers import *
from command_status import print_register_failure, ManagerCommandStatus, print_success


def register(*args):
    params = args[0]

    try:
        peer_name = params[0]
        IPv4_address = params[1]
        m_port = int(params[2])
        p_port = int(params[3])
    except:
        print_register_failure(ManagerCommandStatus.REGISTER_INVALID_COMMAND)
        return

    if peer_name in peers_network:
        print_register_failure(ManagerCommandStatus.REGISTER_PEER_NAME_EXIST)
        return

    peers_network[peer_name] = Peer(peer_name, IPv4_address, m_port, p_port)
    print_success()
    print("TODO: Complete the function")
