import logging
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select
import argparse

from common.utils import send_message, get_message
from common.errors import UnsafePortError
from common.variables import *
from common.decorators import log
from log import server_log_config

logger = logging.getLogger('server')


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


def read_requests(r_clients, all_clients):
    """Read requests from list of clients"""
    responses = {}
    for sock in r_clients:
        client_n = sock.fileno()
        client_peername = sock.getpeername()
        try:
            responses[sock] = get_message(sock)
        except:
            logger.info(f'Client {client_n} {client_peername} was disconnected.')
            all_clients.remove(sock)
    return responses


def write_responses(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try:
                client_message = requests[sock]
                if 'msg' in client_message:
                    client_message['response'] = 200
                    send_message(sock, client_message)
            except TypeError as e:
                logger.exception(f'Is message a dict?')
            except:
                logger.info(f'Client {sock.fileno()} {sock.getpeername()} was disconnected.')
                sock.close()
                all_clients.remove(sock)


def main():
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
        clients = []
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))
        logger.info(f'Server is running on {host}:{str(port)}')
        s.listen(5)
        s.settimeout(0.2)
        while True:
            try:
                client, addr = s.accept()
            except OSError:
                pass
            else:
                logger.debug(f'New client: {addr}')
                clients.append(client)
            finally:
                wait = 1
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass

                responses = read_requests(r, clients)
                if responses:
                    write_responses(responses, w, clients)
            # message = get_message(client)
            # logger.debug(f'Got a message: {message}')
            # answer = process_client_message(message)
            # logger.debug(f'Send an answer {answer} to a client {client.getpeername()}')
            # send_message(client, answer)


if __name__ == '__main__':
    main()
