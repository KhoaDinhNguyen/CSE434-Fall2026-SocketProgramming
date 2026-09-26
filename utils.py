import socket
import gzip
import csv


# Create sockets given bind_port
def create_udp_socket(bind_port: int) -> socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", bind_port))

    return s


# Checks prime number
def is_prime(n: int) -> bool:
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


# Find the next prime number of a number
def next_prime(n: int) -> int:
    candidate = n + 1

    while is_prime(candidate) == False:
        candidate += 1

    return candidate


def compute_hash_table_size(num_records: int) -> int:
    return next_prime(2 * num_records)


def compute_pos_and_id(event_id, table_size, ring_size):
    pos = event_id % table_size
    id = pos % ring_size

    return pos, id


# ====================================================== LOAD DATA ======================================================
FIELD_NAMES = [
    "event_id",
    "state",
    "year",
    "month_name",
    "event_type",
    "cz_type",
    "cz_name",
    "injuries_direct",
    "injuries_indirect",
    "deaths_direct",
    "deaths_indirect",
    "damage_property",
    "damage_crops",
    "tor_f_scale",
]


class StormEvent:
    def __init__(self, values):
        for key, value in zip(FIELD_NAMES, values):
            setattr(self, key, value)

        self.event_id = int(self.event_id)

    def to_string(self):
        return ",".join(str(getattr(self, name)) for name in FIELD_NAMES)

    @classmethod
    def from_string(cls, text):
        return cls(text.split(","))


def load_storms_event(filepath):
    events = []

    with gzip.open(filepath, "rt", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            events.append(StormEvent(row))

    return events
