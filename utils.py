import socket


def create_udp_socket(bind_port: int) -> socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", bind_port))

    return s


def is_prime(n) -> bool:
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


def next_prime(n) -> int:
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
