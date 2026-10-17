import threading
import sys
import peer_info
from peer_commands.register import do_register
from peer_commands.setup_dht import do_setup_dht
from peer_commands.set_id import handle_set_id
from peer_commands.dht_complete import do_dht_complete
from peer_commands.store import handle_store
from peer_commands.teardown_dht import (
    handle_teardown,
    do_teardown,
    do_teardown_complete,
    do_teardown_dht,
)
from peer_commands.reset_id import handle_reset_id, do_reset_id
from peer_commands.leave_dht import do_leave_dht
from peer_commands.rebuild_dht import handle_rebuild_dht, do_rebuild_dht, do_dht_rebuilt
from peer_commands.join_dht import (
    handle_set_right_neighbor,
    handle_update_right_neighbor,
    do_join_dht,
    do_update_right_neighbor,
)

from peer_commands.query_dht import do_query_dht
from peer_commands.find_event import (
    handle_find_event,
    handle_query_success,
    handle_query_failure,
)
from peer_commands.deregister import do_deregister


def listen_for_peer_message():
    while True:
        data, peer_addr = peer_info.p_socket.recvfrom(4096)

        sys.stdout.write("\r" + " " * 80 + "\r")
        data = data.decode("utf-8").strip()

        print(f"\n[RECV] <- {peer_addr}: {data}")

        params = data.split(" ")
        command = params[0]

        match command:
            case "set-id":
                handle_set_id(params[1:], peer_addr)
            case "store":
                handle_store(params[1:])
            case "teardown":
                handle_teardown(params[1:], peer_addr)
            case "reset-id":
                handle_reset_id(params[1:], peer_addr)
            case "rebuild-dht":
                handle_rebuild_dht(peer_addr)
            case "teardown":
                do_teardown(params[1:])
            case "update-right-neighbor":
                handle_update_right_neighbor(params[1:], peer_addr)
            case "set-right-neighbor":
                handle_set_right_neighbor(params[1:], peer_addr)
            case "find-event":
                handle_find_event(params[1:])
            case "SUCCESS":
                if len(params) > 1 and params[1] == "QUERY":
                    handle_query_success(params[2:])
                else:
                    pass
            case "FAILURE":
                if len(params) > 1 and params[1] == "QUERY":
                    handle_query_failure(params[2:])
                else:
                    pass
            case _:
                print(f"Unknown command {data}")

        print("> ", end="", flush=True)


def start_listening():
    thread = threading.Thread(target=listen_for_peer_message, daemon=True)
    thread.start()


def main():
    # This states that the peer needs manager IPv4 address and manager port

    if len(sys.argv) != 3:
        print("Usage: python peer.py <manager-ip> <manager-port>")
        return

    try:
        manager_ip = sys.argv[1]
        manager_port = int(sys.argv[2])
        manager_addr = (manager_ip, manager_port)
    except:
        return

    # ======================================= PEER PROGRAMMING =======================================

    print("Ready for communication...")

    while True:
        # The peer reads commands from the user
        query = input("> ").strip()

        if query == "":
            continue

        params = query.split(" ")
        command = params[0]

        match command:
            case "quit":
                if peer_info.m_socket:
                    peer_info.m_socket.close()
                    peer_info.p_socket.close()
                break
            case "register":
                do_register(params[1:], manager_addr)
                if peer_info.p_socket != None:
                    start_listening()
            case "setup-dht":
                do_setup_dht(params[1:], manager_addr)
            case "dht-complete":
                do_dht_complete(params[1:], manager_addr)
            case "leave-dht":
                do_leave_dht(params[1:], manager_addr)
            case "join-dht":
                do_join_dht(params[1:], manager_addr)
            case "dht-rebuilt":
                do_dht_rebuilt(params[1:], manager_addr)
            case "teardown-dht":
                do_teardown_dht(params[1:], manager_addr)
            case "teardown-complete":
                do_teardown_complete(params[1:], manager_addr)
            case "reset-id":
                do_reset_id(params[1:])
            case "teardown":
                do_teardown(params[1:])
            case "update-right-neighbor":
                do_update_right_neighbor(params[1:])
            case "rebuild-dht":
                do_rebuild_dht()
            case "query-dht":
                do_query_dht(params[1:], manager_addr)
            case "deregister":
                if do_deregister(params[1:], manager_addr):
                    break
            case _:
                print(f"Unknown command: {params[0]}")


if __name__ == "__main__":
    main()
