import socket
import threading


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        hostname = socket.gethostname()
        IP = socket.gethostbyname(hostname)
    finally:
        s.close()
    return IP


# lock for serial queue
lock_queue = threading.Lock()
condition_variable = threading.Condition(lock_queue)
