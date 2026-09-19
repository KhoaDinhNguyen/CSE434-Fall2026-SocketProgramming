import sys
from manager_helpers.setup_dht import setup_dht
import command_status


# Check port number validation
def main() -> bool:
    # Check port number existence
    if len(sys.argv) == 1:
        command_status.print_port_failure("")
        return False

    port_num_str = sys.argv[1]

    try:
        # Port number is an integer
        port_num = int(port_num_str)
        print(f"Manager listening on port {port_num}")
    except:
        command_status.print_port_failure(port_num_str)
        return False

    return True


# Run command
def run():
    print("Manager ready for command")
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
            case "quit":
                break


if __name__ == "__main__":
    if main():
        run()
