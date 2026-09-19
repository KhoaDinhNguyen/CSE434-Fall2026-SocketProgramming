from command_status import *
from .peers import peers_network


class DHT:
    def __init__(self, leader_name: str, num_users: int, year: int):
        self.leader_name = leader_name
        self.num_users = num_users
        self.year = year


dht = None


def setup_dht(*args):
    global dht
    params = args[0]

    try:
        leader_name = params[0]
        num_users = int(params[1])
        year = int(params[2])

    except:
        print_setup_dht_failure(ManagerCommandStatus.SETUP_DHT_INVALID_COMMAND)
        return

    if dht != None:
        print_setup_dht_failure(ManagerCommandStatus.SETUP_DHT_DHT_EXIST)
        return
    if leader_name not in peers_network:
        print_setup_dht_failure(ManagerCommandStatus.SETUP_DHT_PEER_NAME_NOT_EXIST)
        return
    if num_users < 3:
        print_setup_dht_failure(ManagerCommandStatus.SETUP_DHT_LESS_THAN_THREE_USERS)
        return

    dht = DHT(leader_name, num_users, year)

    print_success()
    print("TODO: Complete function")
