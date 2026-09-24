import socket
import sys
from manager_helpers.setup_dht import setup_dht
from manager_helpers.register import register
from manager_helpers.clear import clear
import manager_helpers.dht as dht
from manager_helpers.peers import peers_network
from manager_handlers.register import handle_register
from manager_handlers.setup_dht import handle_setup_dht
import command_status
from utils import create_udp_socket


def main():
    # Check port number existence
    if len(sys.argv) == 1:
        command_status.print_port_failure("")
        return

    port_num_str = sys.argv[1]

    try:
        # Port number is an integer
        port_num = int(port_num_str)
        print(f"Manager listening on port {port_num}...")
    except:
        command_status.print_port_failure(port_num_str)
        return

    # Creates a UDP socket for manager to listen on
    manager_socket = create_udp_socket(port_num)

    while True:
        # Wait for a UDP message instead of using input() Also the 4096 is the maximum size (bytes) of the message that can be received at once
        data, peer_address = manager_socket.recvfrom(4096)

        # Convert the received bytes into a normal Python string
        query = data.decode("utf-8").strip()

        if query == "":
            continue

        params = query.split(" ")
        # This shows what message the manager received for the required trace output
        print(f"[RECV] <- {peer_address}: {query}")

        match params[0]:
            case "setup-dht":
                # Save the result so it can be sent back to the peer
                response = handle_setup_dht(params[1:])
            case "register":
                # Save the result so it can be sent back to the peer
                response = handle_register(params[1:])
            case "clear":
                response = clear()
            case _:
                response = "FAILURE"  # Give unknown commands a response instead of doing nothing

        # Send the command result back to the peer over UDP
        manager_socket.sendto(
            response.encode("utf-8"),
            peer_address,  # Send the response to the peer that originally sent the command
        )

        # Shows the outgoing response for the message trace
        print(f"[SENT] -> {peer_address}: {response}")

        print("=" * 60)


if __name__ == "__main__":
    main()
