import socket


def create_udp_socket(bind_port: int) -> socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", bind_port))

    return s
