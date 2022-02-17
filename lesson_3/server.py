from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import argparse
import json

from common.utils import get_unix_time_str, send_message, get_message
from common.variables import *


def process_client_message(message: dict) -> dict:
    if "action" in message and message['action'] == 'presence'\
            and 'time' in message and 'user' in message:
        answer = {
            "response": RESP_OK,
        }
        print(message)
        return answer
    else:
        answer = {
            "response": RESP_WRONG_REQUEST,
            "error": "Bad Request"
        }
        return answer


def main():
    parser = argparse.ArgumentParser(description='A server')
    parser.add_argument('-a', help='Server\'s address. Default: 127.0.0.1', default=HOST)
    parser.add_argument('-p', help='Server\'s port. Default: 7777', default=PORT)
    args = parser.parse_args()
    host = args.a
    port = int(args.p)
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))
        print(f'Running server on {host}:{port}')
        s.listen(5)
        while True:
            client, addr = s.accept()
            message = get_message(client)
            answer = process_client_message(message)
            send_message(client, answer)


if __name__ == '__main__':
    main()
