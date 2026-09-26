import sys
from manager_handlers.register import handle_register
from manager_handlers.setup_dht import handle_setup_dht
import manager_info
from utils import create_udp_socket


def main():
    # Check port number existence
    if len(sys.argv) == 1:
        print("Usage: python manager.py <manager-port>")
        return

    try:
        # Port number is an integer
        port_num = int(sys.argv[1])
        print(f"Manager listening on port {port_num}...")
    except:
        print("Usage: port is integer number")
        return

    # ======================================= MANAGER PROGRAMMING =======================================

    # Creates a UDP socket for manager to listen on
    manager_socket = create_udp_socket(port_num)

    while True:
        # Wait for a UDP message and 4096 is the maximum size (bytes) of the message that can be received at once
        data, peer_address = manager_socket.recvfrom(4096)

        # Convert the received bytes into a normal Python string
        data = data.decode("utf-8").strip()

        if data == "":
            continue

        # command, params = data.split(" ", 1)
        params = data.split(" ")
        command = params[0]

        # Shows what message the manager received for the required trace output
        print(f"[RECV] <- {peer_address}: {data}")

        # Special case
        if manager_info.is_waiting_dht_complete:
            leader_info = manager_info.peers_network[manager_info.dht_leader_name]

            # Only leaders can send dht-complete
            leader_address = (leader_info.ip, leader_info.m_port)
            print(leader_address)
            print(peer_address)
            if command != "dht-complete" or leader_address != peer_address:
                response = "FAILURE"
            else:
                response = "SUCCESS"
                manager_info.is_waiting_dht_complete = False
                print("Leader has completed the setup-dht subtasks")
        else:
            match command:
                case "setup-dht":
                    response = handle_setup_dht(params[1:])
                case "register":
                    response = handle_register(params[1:])
                case _:
                    response = "FAILURE"  # Give unknown commands a response instead of doing nothing

        # Send the command result back to the peer over UDP and log it
        manager_socket.sendto(response.encode("utf-8"), peer_address)
        print(f"[SENT] -> {peer_address}: {response}")

        print("=" * 60)


if __name__ == "__main__":
    main()
