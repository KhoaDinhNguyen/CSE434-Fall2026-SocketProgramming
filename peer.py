import socket
import sys


def main():
    # Chuan: This states that the peer needs manager IPv4 address and manager port
    if len(sys.argv) != 3:
        print("Usage: python peer.py <manager-ip> <manager-port>")
        return

    manager_ip = sys.argv[1]
    manager_port = int(sys.argv[2])

    # Chuan: This creates the UDP socket for the peer to send commands to the manager and receive responses
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # Chuan: The peer reads commands from the user
        command = input("> ").strip()

        if command == "":
            continue

        # Chuan: This sends the command to the manager over UDP
        peer_socket.sendto(command.encode("utf-8"),(manager_ip, manager_port),)

        # Chuan: Wait for manager response
        data, _ = peer_socket.recvfrom(4096)

        # This either prints SUCCESS or FAILURE
        print(data.decode("utf-8"))


if __name__ == "__main__":
    main()