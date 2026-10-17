import random
import peer_info
from utils import compute_pos_and_id, StormEvent, FIELD_NAMES


def handle_find_event(args):
    try:
        event_id = int(args[0])

        # 3-tuple of the peer that originally issued the query
        source_name = args[1]
        source_ip = args[2]
        source_port = int(args[3])

        # id-seq is optional on the first find-event message
        if len(args) >= 5 and args[4] != "":
            id_seq = [int(node_id) for node_id in args[4].split(",")]
        else:
            id_seq = []

    except:
        print("Invalid find-event request")
        return

    # Add this peer to the sequence of visited DHT nodes
    if peer_info.id not in id_seq:
        id_seq.append(peer_info.id)

    # Calculate where the event should be located
    pos, target_id = compute_pos_and_id(
        event_id,
        peer_info.hash_table_size,
        peer_info.ring_size
    )

    print(
        f"Searching event_id={event_id} "
        f"at node id={peer_info.id}, pos={pos}, target_id={target_id}"
    )

    # Check this peer's local hash table
    event = peer_info.local_hash_table.find(pos, event_id)
    if event is not None:
        send_query_success(
            event,
            id_seq,
            (source_ip, source_port)
        )
        return 

    # Find DHT peers that have not been visited yet
    unvisited_ids = [
        node_id
        for node_id in peer_info.dht_peers
        if node_id not in id_seq
    ]

    # No peers remain -> event does not exist in the DHT
    if len(unvisited_ids) == 0:
        send_query_failure(
            event_id,
            id_seq,
            (source_ip, source_port)
        )
        return

    # Hot-potato: randomly choose the next unvisited peer
    next_id = random.choice(unvisited_ids)

    next_name, next_ip, next_port = peer_info.dht_peers[next_id]
    next_addr = (next_ip, next_port)

    # Add next peer to id-seq before forwarding
    next_id_seq = id_seq + [next_id]
    id_seq_text = ",".join(str(node_id) for node_id in next_id_seq)

    message = (
        f"find-event {event_id} "
        f"{source_name} {source_ip} {source_port} "
        f"{id_seq_text}"
    )

    peer_info.p_socket.sendto(
        message.encode("utf-8"),
        next_addr
    )

    print(
        f"[FORWARD] -> {next_name} {next_addr}: {message}"
    )


def send_query_success(event, id_seq, source_addr):
    id_seq_text = ",".join(str(node_id) for node_id in id_seq)

    # QUERY distinguishes this SUCCESS from other SUCCESS messages
    message = (
        f"SUCCESS QUERY {id_seq_text} "
        f"{event.to_string()}"
    )

    peer_info.p_socket.sendto(
        message.encode("utf-8"),
        source_addr
    )

    print(f"[SEND] -> {source_addr}: SUCCESS QUERY")


def send_query_failure(event_id, id_seq, source_addr):
    id_seq_text = ",".join(str(node_id) for node_id in id_seq)

    message = (
        f"FAILURE QUERY {event_id} {id_seq_text}"
    )

    peer_info.p_socket.sendto(
        message.encode("utf-8"),
        source_addr
    )

    print(f"[SEND] -> {source_addr}: {message}")


def handle_query_success(args):
    id_seq = args[0]

    # Rejoin because storm-event fields may contain spaces
    event_data = " ".join(args[1:])
    event = StormEvent.from_string(event_data)

    print("\nQuery SUCCESS")

    for field_name in FIELD_NAMES:
        print(f"{field_name}: {getattr(event, field_name)}")

    print(f"id-seq: {id_seq}")


def handle_query_failure(args):
    event_id = args[0]

    print(f"Storm event {event_id} not found in the DHT.")

    if len(args) > 1:
        print(f"id-seq: {args[1]}")