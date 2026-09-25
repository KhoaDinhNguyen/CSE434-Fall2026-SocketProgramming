import peer_info
from .set_id import do_set_id
import time
from .store import populate_dht
from data import load_storms_event
from utils import compute_hash_table_size


def do_setup_dht(params, manager_addr):
    leader_name = params[0]
    nusers = int(params[1])
    year = int(params[2])

    if leader_name != peer_info.name:
        return

    # Send to manager
    message = f"setup-dht {leader_name} {nusers} {year}"
    print(f"[SEND] -> {manager_addr}: {message}")
    peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)

    # Receive data
    response, _ = peer_info.m_socket.recvfrom(4096)
    response = response.decode("utf-8")

    print(f"[RECV] <- {manager_addr}: {response}")

    # DHT creation continue
    table = response.split("\n")
    table = table[1:]

    # load data
    events = load_storms_event(f"details-{year}.csv.gz")
    l = len(events)
    table_size = compute_hash_table_size(l)
    peer_info.counts = [0] * nusers

    # set-id
    for idx in range(len(table)):
        row = table[idx]
        r_row = table[0] if idx == len(table) - 1 else table[idx + 1]

        params = row.split(" ")
        r_params = r_row.split(" ")

        ip, p_port, id, ring_size = params[1], params[2], idx, nusers
        r_name, r_ip, r_port = r_params

        do_set_id([ip, p_port, id, ring_size, r_name, r_ip, r_port, table_size])

        time.sleep(2)

    # populate data
    populate_dht(events)
