from data import StormEvent
from utils import compute_pos_and_id
import peer_info


def populate_dht(events):
    for event in events:
        pos, target_id = compute_pos_and_id(
            event.event_id, peer_info.hash_table_size, peer_info.ring_size
        )

        peer_info.counts[target_id] += 1

        if target_id == peer_info.id:
            peer_info.local_hash_table.insert(pos, event)
        else:
            forward_store(target_id, pos, event)

    print("Records distribution:")
    for node_id, count in enumerate(peer_info.counts):
        print(f"  Node id={node_id}: {count} records")


def forward_store(target_id, pos, event):
    message = f"store {target_id} {pos} {event.to_string()}"
    r_neighbor = (peer_info.r_ip, peer_info.r_port)

    peer_info.p_socket.sendto(message.encode("utf-8"), r_neighbor)

    print(f"[SEND] -> {r_neighbor}: {message}")


def handle_store(args):
    target_id, pos_data = args.split(" ", 1)
    pos, data = pos_data.split(" ", 1)

    target_id = int(target_id)
    pos = int(pos)

    event = StormEvent.from_string(data)

    if target_id == peer_info.id:
        peer_info.local_hash_table.insert(pos, event)
        print(f"Stored event_id={event.event_id} at table={target_id} pos={pos}")
    else:
        forward_message = f"store {target_id} {pos} {event.to_string()}"
        r_neighbor = (peer_info.r_ip, peer_info.r_port)
        peer_info.p_socket.sendto(forward_message.encode("utf-8"), r_neighbor)

        print(f"[FORWARD] -> {r_neighbor}: {forward_message}")
