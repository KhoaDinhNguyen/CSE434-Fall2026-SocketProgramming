import peer_info
from .store import populate_dht
from utils import load_storms_event
import time


def do_rebuild_dht():
    r_addr = (peer_info.r_ip, peer_info.r_port)

    message = f"rebuild-dht"
    peer_info.p_socket.sendto(message.encode("utf-8"), r_addr)

    print(f"[SEND]-> {r_addr}: {message}")


def handle_rebuild_dht(peer_addr):
    # loads data
    events = load_storms_event(f"details-{peer_info.year}.csv.gz")
    peer_info.counts = [0] * peer_info.ring_size

    # populate data
    populate_dht(events)

    time.sleep(5)

    message = f"SUCCESS"
    peer_info.p_socket.sendto(message.encode("utf-8"), peer_addr)

    print(f"[SEND] -> {peer_addr}: {message}")


def do_dht_rebuilt(args, manager_addr):
    try:
        peer_name = args[0]
        leader_name = args[1]

        # Send the command to manager
        message = f"dht-rebuilt {peer_name} {leader_name}"

        peer_info.m_socket.sendto(message.encode("utf-8"), manager_addr)
        print(f"[SEND] -> {manager_addr}: {message}")

        # Receive response from manager
        response, _ = peer_info.m_socket.recvfrom(4096)
        response = response.decode("utf-8")

        print(f"[RECV] <- {manager_addr}: {response}")

    except:
        print("Invalid request")
        return
