"""
peer_info.py contains all global variables for one manager process
"""

# state information
name = None
state = None
m_socket = None
p_socket = None
ip = None
p_port = None
m_port = None

# ring topology
id = -1
ring_size = -1
year = -1

# All peers in the DHT
# id -> (name, ip, p_port)
dht_peers = {}

# right neighbor
r_name = None
r_ip = None
r_port = None

# counts
hash_table_size = -1
local_hash_table = None
counts = {}


class LocalHashTable:
    def __init__(self, size):
        self.size = size
        self.mem = [[] for _ in range(size)]

    def insert(self, pos, storm_event):
        self.mem[pos].append(storm_event)

    def clear(self):
        self.mem = [[] for _ in range(self.size)]

    def find(self, pos, event_id):
        for event in self.mem[pos]:
            if event.event_id == event_id:
                return event
        return None


def print_dht_peers() -> None:
    print("Updated DHT peers")
    for peer_id, (name, ip, p_port) in dht_peers.items():
        print(f"  Node id={peer_id}: {name} {ip} {p_port}")


def dht_peers_to_str() -> str:
    return ";".join(
        f"{peer_id},{name},{ip},{port}"
        for peer_id, (name, ip, port) in sorted(dht_peers.items())
    )


def str_to_dht_peers(s: str):
    peers = {}
    if not s:
        return peers

    for entry in s.split(";"):
        peer_id, name, ip, port = entry.split(",")
        peers[int(peer_id)] = (name, ip, int(port))

    return peers


def reorder_dht_peers(
    new_leader_name: str,
    is_leave: bool,
    new_peer_name: str = "",
    new_peer_ip: str = "",
    new_peer_port: int = -1,
):
    """
    Rotate the ring so `new_leader_name` becomes ID 0, then either:
      - drop the last peer (the one just before the new leader) if is_leave, or
      - append `new_peer` at the end if joining.
    Assumes IDs in dht_peers are exactly 0..n-1 and the new leader is present.
    """
    # Peers in ID order
    original_order = [dht_peers[i] for i in range(len(dht_peers))]
    leader_idx = 0

    for i, (name, _, _) in enumerate(original_order):
        if name == new_leader_name:
            leader_idx = i
            break

    new_order = original_order[leader_idx:] + original_order[:leader_idx]

    if is_leave:
        # Remove last element
        new_order.pop()
    else:
        new_order.append((new_peer_name, new_peer_ip, new_peer_port))

    # Reassign dictionary
    dht_peers.clear()
    dht_peers.update(enumerate(new_order))
