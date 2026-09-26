"""
manager_info.py contains all global variables for one manager process
"""


# Peer Object
class Peer:
    def __init__(self, name: str, ip: str, m_port: int, p_port: int):
        self.name = name
        self.ip = ip
        self.m_port = m_port
        self.p_port = p_port
        self.state = "FREE"
        self.identifier = -1
        self.ring_size = -1


# Mapping <peer_name>: <Peer>
# All peers in network
peers_network = {}

# Only peers in Distributed Hash Table (Leader + INDHT)
peers_dht_table = []

# Records used pots
used_ports = set()

# State information
dht_leader_name = None
dht_ring_size = 0
dht_year = 0
has_dht_exist = False
is_waiting_dht_complete = False


# Create a table listing peerse in DHT
def output_peers_dht_table():
    output = "\n"

    for peer_name in peers_dht_table:
        peer = peers_network[peer_name]

        output += f"{peer.name} {peer.ip} {peer.p_port}\n"

    output = output[:-1]

    return output
