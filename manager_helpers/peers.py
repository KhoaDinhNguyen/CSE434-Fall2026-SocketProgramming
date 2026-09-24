from enum import Enum


class PeerState(Enum):
    FREE = 1
    LEADER = 2
    INDHT = 3


class Peer:
    def __init__(self, peer_name: str, IPv4_address: str, m_port: str, p_port):
        self.peer_name = peer_name
        self.IPv4_address = IPv4_address
        self.m_port = m_port
        self.p_port = p_port
        self.state = PeerState.FREE
        self.identifier = -1
        self.ring_size = -1


peers_network = {}
