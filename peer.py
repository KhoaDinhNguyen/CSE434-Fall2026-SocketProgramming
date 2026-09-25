import threading
import sys
import peer_info
from peer_commands.register import do_register
from peer_commands.setup_dht import do_setup_dht
from peer_commands.set_id import handle_set_id
from peer_commands.dht_complete import do_dht_complete
from peer_commands.store import handle_store


def listen_for_peer_message():
    while True:
        data, peer_addr = peer_info.p_socket.recvfrom(4096)

        sys.stdout.write("\r" + " " * 80 + "\r")
        data = data.decode("utf-8").strip()

        print(f"\n[RECV] <- {peer_addr}: {data}")

        command, args = data.split(" ", 1)

        match command:
            case "set-id":
                handle_set_id(args, peer_addr)
            case "store":
                handle_store(args)
            case "Has":
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

    manager_ip = sys.argv[1]
    manager_port = int(sys.argv[2])
    manager_addr = (manager_ip, manager_port)

    print("Ready for communication...")

    while True:
        # The peer reads commands from the user
        command = input("> ").strip()

        if command == "":
            continue

        params = command.split(" ")

        match params[0]:
            case "quit":
                break
            case "register":
                do_register(params[1:], manager_addr)
                if peer_info.p_socket != None:
                    start_listening()
            case "setup-dht":
                do_setup_dht(params[1:], manager_addr)
            case "dht-complete":
                do_dht_complete(manager_addr)

            case _:
                print(f"Unknown command: {params[0]}")

        # # This sends the command to the manager over UDP
        # peer_socket.sendto(
        #     command.encode("utf-8"),
        #     (manager_ip, manager_port),
        # )
        # print(f"[SEND] -> {command}")

        # # Wait for manager response
        # data, _ = peer_socket.recvfrom(4096)

        # # This either prints SUCCESS or FAILURE
        # print(f"[RECV] <- {data.decode("utf-8")}")

        # params = command.split(" ")
        # print(data)

        # if data.decode("utf-8") == success_code and params[0] == "register":
        #     m_port, p_port = int(params[3]), int(params[4])

        #     m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     m_socket.bind(("0.0.0.0", m_port))

        #     p_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     p_socket.bind(("0.0.0.0", p_port))

        #     m_data = peer_socket.recvfrom(4096)
        #     p_data = peer_socket.recvfrom(4096)

        #     print("OPEN")

        #     print(m_data)
        #     print(p_data)


if __name__ == "__main__":
    main()
