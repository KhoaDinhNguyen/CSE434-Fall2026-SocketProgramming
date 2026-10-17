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

# leave-dht
is_teardown_request = False


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
