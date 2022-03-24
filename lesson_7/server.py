import logging
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import argparse
import time

from common.utils import send_message, get_message
from common.errors import UnsafePortError
from common.variables import *
from common.decorators import log
import select
from log import server_log_config


@log
def process_client_message(message: dict) -> dict:
    if "action" in message and message['action'] == 'presence'\
            and 'time' in message and 'user' in message:
        answer = {
            "response": RESP_OK,
        }
        return answer
    elif "action" in message and message['action'] == 'msg'\
            and 'time' in message and 'user' in message:
        answer = {
            "response": RESP_OK,
            "from": message['user']['account_name'],
            "text": message['text'],
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
    clients = []
    messages = []

    if not 1024 < port < 65536:
        logger.critical('Please, specify safe port (1024-65536)')
        raise UnsafePortError

    with socket(AF_INET, SOCK_STREAM) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))
        s.settimeout(0.5)
        logger.info(f'Server is running on {host}:{str(port)}')
        s.listen(5)

        while True:
            try:
                client, addr = s.accept()
            except OSError as err:
                if err.errno:
                    print(err.errno)
                pass
            else:
                clients.append(client)
                logger.debug(f'New client: {addr}')

            recv_data_lst = []
            send_data_lst = []

            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        message = get_message(client_with_message)
                        logger.debug(f'Got a message: {message}')
                        answer = process_client_message(message)
                        if 'text' in answer:
                            messages.append(answer)
                        else:
                            send_message(client_with_message, answer)
                    except Exception as e:
                        logger.info(f'Client {client.getpeername()} was disconnected')
                        clients.remove(client_with_message)

            if messages and send_data_lst:
                answer = {
                    "action": "message",
                    "from": messages[0]['from'],
                    "text": messages[0]['text'],
                    "time": time.time(),
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        logger.debug(f'Sending an answer {answer} to a client {client.getpeername()}')
                        send_message(waiting_client, answer)
                    except Exception as e:
                        logger.info(f'Client {client.getpeername()} was disconnected')
                        waiting_client.close()
                        clients.remove(waiting_client)


if __name__ == '__main__':
    main()
