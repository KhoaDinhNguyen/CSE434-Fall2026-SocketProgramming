import manager_info

def handle_deregister(args):
    if has_invalid_deregister_args(args):
        return "FAILURE"

    peer_name = args[0]
    peer = manager_info.peers_network[peer_name]

    # Free ports so they can be used again later
    manager_info.used_ports.discard(peer.m_port)
    manager_info.used_ports.discard(peer.p_port)

    # Remove peer from manager state
    del manager_info.peers_network[peer_name]
    return "SUCCESS"

def has_invalid_deregister_args(args):
    try:
        peer_name = args[0]

        # Peer must be registered
        if peer_name not in manager_info.peers_network:
            return True

        # Only FREE peers may deregister
        if manager_info.peers_network[peer_name].state != "FREE":
            return True
    except:
        
        return True
    
    return False