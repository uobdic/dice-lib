def current_fqdn() -> str:
    """Returns fully-qualified domain main (FQDN) of current machine"""
    import socket

    return socket.getfqdn()
