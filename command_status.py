# File that contains all command print based on their status
from enum import Enum


# STATUS CODE
class ManagerCommandStatus(Enum):
    SETUP_DHT_INVALID_COMMAND = 1
    SETUP_DHT_LESS_THAN_THREE_USERS = 2
    SETUP_DHT_DHT_EXIST = 3
    SETUP_DHT_PEER_NAME_NOT_EXIST = 6
    REGISTER_INVALID_COMMAND = 4
    REGISTER_PEER_NAME_EXIST = 5


failure_code = "FAILURE"
success_code = "SUCCESS"


def print_success():
    print(success_code)


def print_port_failure(port: str):
    print(f"{failure_code}: ", end="")

    if port == "":
        print("No inititalized port")
    else:
        print(f"Invalid port number, should be integer")


def print_setup_dht_failure(status: ManagerCommandStatus):
    print(f"{failure_code}: ", end="")

    match status:
        case ManagerCommandStatus.SETUP_DHT_INVALID_COMMAND:
            print(
                "Invalid command. Check the command again: setup-dht <peer_name, string> <n, integer> <YYYY, integer>"
            )
        case ManagerCommandStatus.SETUP_DHT_LESS_THAN_THREE_USERS:
            print("Not enough users for network")
        case ManagerCommandStatus.SETUP_DHT_DHT_EXIST:
            print("DHT already exists")
        case ManagerCommandStatus.SETUP_DHT_PEER_NAME_NOT_EXIST:
            print("Peer name does not exist")


def print_register_failure(status: ManagerCommandStatus):
    print(f"{failure_code}: ", end="")

    match status:
        case ManagerCommandStatus.REGISTER_INVALID_COMMAND:
            print(
                "Invalid command. Check the comman again: register <peer_name, string> <IPv4-address, string> <m-port, int> <p-port, int>"
            )

        case ManagerCommandStatus.REGISTER_PEER_NAME_EXIST:
            print("Peer name already exists")
