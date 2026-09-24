import socket
from . import peers
from command_status import (
    failure_code,
    success_code,
)  # We can return these codes to manager.py instead of just printing them


def register(*args):
    params = args[0]

    if len(params) != 4:  # register needs to have 4 parameters
        return failure_code  # Return FAILURE so manager.py can send it back to the peer

    try:
        peer_name = params[0]
        IPv4_address = params[1]
        m_port = int(params[2])
        p_port = int(params[3])
    except (ValueError, IndexError):
        return failure_code  # Changed it to return FAILURE so manager.py can send it back to the peer instead of printing it

    # The peer name has to be alphabetic plus no more than 15 characters
    if not peer_name.isalpha() or len(peer_name) > 15:
        return failure_code

    if peer_name in peers.peers_network:
        return failure_code  # return FAILURE so manager.py can send it back to the peer instead of printing it
    if m_port == p_port:  # manager and peer ports must be different
        return failure_code

    # This checks ports that have been already used by registered peers
    for peer in peers.peers_network.values():
        if m_port in (peer.m_port, peer.p_port) or p_port in (peer.p_port, peer.m_port):
            return failure_code  # returns FAILURE for duplicate ports

    peers.peers_network[peer_name] = peers.Peer(peer_name, IPv4_address, m_port, p_port)

    print(f"[REGISTER] {peer_name} registered")

    return success_code
