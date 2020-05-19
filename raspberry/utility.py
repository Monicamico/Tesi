import socket
import threading


def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


# lock for serial queue
lock_queue = threading.Lock()
condition_variable = threading.Condition(lock_queue)