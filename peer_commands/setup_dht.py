import peer_info
from .set_id import do_set_id
import time
from .store import populate_dht
from data import load_storms_event
from utils import compute_hash_table_size


def do_setup_dht(args, manager_addr):
    if has_invalid_setup_dht_args(args):
        print("Invalid request")
        return

    leader_name = args[0]
    ring_size = int(args[1])
    year = int(args[2])

    # Send requests to the manager
    message = f"setup-dht {leader_name} {ring_size} {year}"
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    print(f"[SEND] -> {manager_addr}: {message}")

    # Receives response from managers
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")

    # Stop the DHT creation when the response is Failure
    if response == "FAILURE":
        return

    # DHT creation continue
    table = response.split("\n")
    table = table[1:]

    # loads data
    events = load_storms_event(f"details-{year}.csv.gz")
    l = len(events)
    table_size = compute_hash_table_size(l)
    peer_info.counts = [0] * ring_size

    # Runs set-id around the ring topology
    for idx in range(len(table)):
        row = table[idx]
        r_row = table[0] if idx == len(table) - 1 else table[idx + 1]

        # Peer ip information
        params = row.split(" ")
        ip, p_port, id, ring_size = params[1], params[2], idx, ring_size

        # Right neightbour information
        r_params = r_row.split(" ")
        r_name, r_ip, r_port = r_params

        do_set_id([id, ring_size, r_name, r_ip, r_port, table_size], (ip, int(p_port)))

        # Wait for response
        time.sleep(2)

    # populate data
    populate_dht(events)


def has_invalid_setup_dht_args(args):
    try:
        leader_name = args[0]
        ring_size = int(args[1])
        year = int(args[2])
    except:
        return True

    return False
