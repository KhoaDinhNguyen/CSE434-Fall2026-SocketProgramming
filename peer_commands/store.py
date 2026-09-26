from utils import compute_pos_and_id, StormEvent
import peer_info


def populate_dht(events):
    for event in events:
        pos, target_id = compute_pos_and_id(
            event.event_id, peer_info.hash_table_size, peer_info.ring_size
        )

        # Stores records at each node
        peer_info.counts[target_id] += 1

        # If the target_id matches with process id, stores data at local
        # If not, forward the records to right neighbour
        if target_id == peer_info.id:
            peer_info.local_hash_table.insert(pos, event)
        else:
            message = f"store {target_id} {pos} {event.to_string()}"
            r_neighbor = (peer_info.r_ip, peer_info.r_port)
            peer_info.p_socket.sendto(message.encode("utf-8"), r_neighbor)

            print(f"[FORWARD] -> {r_neighbor}: {message}")

    # Configure the nodes
    print("Records distribution:")
    for node_id, count in enumerate(peer_info.counts):
        print(f"  Node id={node_id}: {count} records")


def handle_store(args):
    target_id = int(args[0])
    pos = int(args[1])
    data = args[2]

    # Convert the event object from string
    event = StormEvent.from_string(data)

    if target_id == peer_info.id:
        peer_info.local_hash_table.insert(pos, event)
        print(f"Stored event_id={event.event_id} at pos={pos}")
    else:
        forward_message = f"store {target_id} {pos} {data}"
        r_neighbor = (peer_info.r_ip, peer_info.r_port)
        peer_info.p_socket.sendto(forward_message.encode("utf-8"), r_neighbor)

        print(f"[FORWARD] -> {r_neighbor}: {forward_message}")
