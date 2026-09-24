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
has_assigned_identifers = False
has_contruct_dht = False
has_signal = False


def output_peers_dht_table():
    output = "-" * 30 + "\n" + "In-DHT Peers Table\n"

    for peer_name in peers_dht_table:
        peer = peers_network[peer_name]

        output += f"{peer.name} {peer.ip} {peer.p_port}\n"

    return output


def output_leader_task():
    output = "-" * 30 + "\n" + "Leader's tasks:\n"

    output += (
        f"Assign identifers and neighbors [{"O" if has_assigned_identifers else "X"}]\n"
    )

    output += f"Construct the local DHTs [{"O" if has_contruct_dht else "X"}]\n"
    output += f"Print configuration and signal completion DHT set up [{"O" if has_signal else "X"}]"

    return output
