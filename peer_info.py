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

#All peers in the DHT
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
    def find(self, pos, even_id):
        for event in self.mem[pos]:
            if event.event_id == even_id:
                return event
        return None
