import time
from lesson_3.common.variables import BYTES_RECV_SIZE
import json


def send_message(sock, message: dict, encoding='ascii'):
    message = json.dumps(message)
    sock.send(message.encode(encoding))


def get_message(sock, encoding='ascii') -> dict:
    response = sock.recv(BYTES_RECV_SIZE)
    if isinstance(response, bytes):
        json_response = response.decode(encoding)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def get_unix_time_str():
    unix_time_str = time.ctime(time.time()) + '\n'
    return unix_time_str
