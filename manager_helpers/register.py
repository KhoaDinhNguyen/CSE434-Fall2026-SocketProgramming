from .peers import *
from command_status import failure_code, success_code  # Chuan: We can return these codes to manager.py instead of just printing them


def register(*args):
    params = args[0]

    if len(params) != 4:  # Chuan: register needs to have 4 parameters
        return failure_code  # Chuan: Return FAILURE so manager.py can send it back to the peer

    try:
        peer_name = params[0]
        IPv4_address = params[1]
        m_port = int(params[2])
        p_port = int(params[3])
    except (ValueError, IndexError):  # Chuan: Just to catch errors
        return failure_code  # Chuan: Changed it to return FAILURE so manager.py can send it back to the peer instead of printing it

    if not peer_name.isalpha() or len(peer_name) > 15:  # Chuan: The peer name has to be alphabetic plus no more than 15 characters
        return failure_code 
    
    if peer_name in peers_network:
        return failure_code  # Chuan: I changed it to return FAILURE so manager.py can send it back to the peer instead of printing it
    if m_port == p_port:  # Chuan: manager and peer ports must be different
        return failure_code  

    for peer in peers_network.values():  # Chuan: This checks ports that have been already used by registered peers
        if m_port == peer.m_port or m_port == peer.p_port or p_port == peer.m_port or p_port == peer.p_port:  
            return failure_code  # Chuan: returns FAILURE for duplicate ports

    peers_network[peer_name] = Peer(peer_name, IPv4_address, m_port, p_port)

    print(f"[REGISTER] {peer_name} registered") 

    return success_code  