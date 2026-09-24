from . import peers


class DHT:
    def __init__(self, leader_name: str, num_users: int, year: int):
        self.leader_name = leader_name
        self.num_users = num_users
        self.year = year
        self.peers_in_dht = []
        self.assignIdAndNeighbour = False
        self.constructLocalDhHT = False
        self.signalDHTSetUp = False

    def output_peers_network(self) -> str:
        output = "Peerss table\n"

        for peer_name in self.peers_in_dht:
            peer = peers.peers_network[peer_name]

            output += f"{peer.peer_name} {peer.IPv4_address} {peer.p_port}\n"

        return output


dhtInstance = None
