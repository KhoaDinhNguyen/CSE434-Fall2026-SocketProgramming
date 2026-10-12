import threading
import sys
import peer_info
from peer_commands.register import do_register
from peer_commands.setup_dht import do_setup_dht
from peer_commands.set_id import handle_set_id
from peer_commands.dht_complete import do_dht_complete
from peer_commands.store import handle_store
from peer_commands.teardown_dht import handle_teardown, do_teardown
from peer_commands.reset_id import handle_reset_id, do_reset_id
from peer_commands.leave_dht import do_leave_dht
from peer_commands.rebuild_dht import handle_rebuild_dht, do_rebuild_dht, do_dht_rebuilt


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
            case "SUCCESS":
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
            case "reset-id":
                do_reset_id(params[1:])
            case "teardown":
                do_teardown(params[1:])
            case "rebuild-dht":
                do_rebuild_dht()
            case "dht-rebuilt":
                do_dht_rebuilt(params[1:], manager_addr)
            case _:
                print(f"Unknown command: {params[0]}")


if __name__ == "__main__":
    main()
