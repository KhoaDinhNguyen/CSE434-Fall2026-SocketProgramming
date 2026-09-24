import socket
import sys
from command_status import success_code
from peer_commands.register import do_register
from peer_commands.setup_dht import do_setup_dht


def main():
    # This states that the peer needs manager IPv4 address and manager port
    if len(sys.argv) != 3:
        print("Usage: python peer.py <manager-ip> <manager-port>")
        return

    manager_ip = sys.argv[1]
    manager_port = int(sys.argv[2])
    manager_addr = (manager_ip, manager_port)

    print("Communicating...")

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
            case "setup-dht":
                do_setup_dht(params[1:], manager_addr)
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
