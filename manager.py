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

    while True:
        query = input("> ")
        if query == "":
            continue

        params = query.split(" ")
        command = params[0]

        print(params[1:])
        match command:
            case "setup-dht":
                setup_dht(params[1:])
            case "register":
                register(params[1:])
            case "quit":
                break


if __name__ == "__main__":
    main()
