import logging
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import argparse

from common.utils import send_message, get_message
from common.errors import UnsafePortError
from common.variables import *
from common.decorators import log
from log import server_log_config


@log
def process_client_message(message: dict) -> dict:
    if "action" in message and message['action'] == 'presence'\
            and 'time' in message and 'user' in message:
        answer = {
            "response": RESP_OK,
        }
        return answer
    else:
        answer = {
            "response": RESP_WRONG_REQUEST,
            "error": "Bad Request"
        }
        return answer


def main():
    logger = logging.getLogger('server')
    parser = argparse.ArgumentParser(description='A server')
    parser.add_argument('-a', help='Server\'s address. Default: 127.0.0.1', default=HOST)
    parser.add_argument('-p', help='Server\'s port. Default: 7777', default=PORT)
    args = parser.parse_args()
    host = args.a
    port = int(args.p)
    if not 1024 < port < 65536:
        logger.critical('Please, specify safe port (1024-65536)')
        raise UnsafePortError
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))
        logger.info(f'Server is running on {host}:{str(port)}')
        s.listen(5)
        while True:
            client, addr = s.accept()
            logger.debug(f'New client: {addr}')
            message = get_message(client)
            logger.debug(f'Got a message: {message}')
            answer = process_client_message(message)
            logger.debug(f'Send an answer {answer} to a client {client.getpeername()}')
            send_message(client, answer)


if __name__ == '__main__':
    main()
