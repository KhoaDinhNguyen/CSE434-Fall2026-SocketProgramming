import socket
import sys
from manager_helpers.setup_dht import setup_dht
from manager_helpers.register import register
import command_status


def main():
    # Check port number existence
    if len(sys.argv) == 1:
        command_status.print_port_failure("")
        return

    port_num_str = sys.argv[1]

    try:
        # Port number is an integer
        port_num = int(port_num_str)
        print(f"Manager listening on port {port_num} and ready for command")
    except:
        command_status.print_port_failure(port_num_str)
        return

    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Chuan: Creates a UDP socket for manager to listen on

    manager_socket.bind(("0.0.0.0", port_num))  # Chuan: Make the manager listen on the port given in the command line
    while True:
        data, peer_address = manager_socket.recvfrom(4096)  # Chuan: Wait for a UDP message instead of using input() Also the 4096 is the maximum size (bytes) of the message that can be received at once
        query = data.decode("utf-8").strip()  # Chuan: Convert the received bytes into a normal Python string

        if query == "":
            continue

        params = query.split(" ")  
        command = params[0]

        print(f"[RECEIVED] {query}")  # Chuan: This shows what message the manager received for the required trace output

        match command:
            case "setup-dht":
                response = setup_dht(params[1:])  # Chuan: Save the result so it can be sent back to the peer

            case "register":
                response = register(params[1:])  # Chuan: Save the result so it can be sent back to the peer

            case _:
                response = "FAILURE"  # Chuan: Give unknown commands a response instead of doing nothing

        manager_socket.sendto(  # Chuan: Send the command result back to the peer over UDP
            response.encode("utf-8"),  # Chuan: Convert SUCCESS/FAILURE from a string into bytes
            peer_address,  # Chuan: Send the response to the peer that originally sent the command
        )

        print(f"[SENT] {response}")  # Chuan: Shows the outgoing response for the message trace


if __name__ == "__main__":
    main()