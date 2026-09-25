name = None
state = None

# socket
m_socket = None
p_socket = None

# ring topology
id = -1
ring_size = -1

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
        self.mem = [None] * size

    def insert(self, pos, storm_event):
        self.mem[pos] = storm_event
