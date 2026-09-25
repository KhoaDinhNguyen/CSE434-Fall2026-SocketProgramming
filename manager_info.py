class Peer:
    def __init__(self, name: str, ip: str, m_port: str, p_port):
        self.name = name
        self.ip = ip
        self.m_port = m_port
        self.p_port = p_port
        self.state = "FREE"
        self.identifier = -1
        self.ring_size = -1


peers_network = {}
dhtInstance = None
used_ports = set()

dht_leader_name = None
dht_nusers = 0
dht_years = 0

peers_dht_table = []

is_waiting_dht_complete = False


def output_peers_dht_table():
    output = "\n"

    for peer_name in peers_dht_table:
        peer = peers_network[peer_name]

        output += f"{peer.name} {peer.ip} {peer.p_port}\n"

    output = output[:-1]

    return output
