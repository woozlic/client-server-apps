import logging
import time
from socket import AF_INET, SOCK_STREAM, socket
import argparse
import threading

from common.variables import PORT, ACT_PRESENCE, HOST, ACT_MESSAGE
from common.utils import get_unix_time_str, send_message, get_message
import log.client_log_config
from common.decorators import log

logger = logging.getLogger('client')


@log
def handle_answer(message):
    GOOD_RESPONSES = {
        200: 'Status: Online!'
    }
    BAD_RESPONSES = (400, 404, 500)
    if message['response'] in BAD_RESPONSES:
        logger.info(message['error']['error'])
    elif message['response'] in GOOD_RESPONSES.keys():
        logger.info(GOOD_RESPONSES[message['response']])
    else:
        logger.error(f'Wrong message: {str(message)}')



@log
def create_presence(account_name='guest'):

    presence = {
        "action": ACT_PRESENCE,
        "time": get_unix_time_str(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "online"
        }
    }
    return presence

@log
def create_message(message: str, to: str, account_name: str = 'guest'):

    message_dict = {
        "action": ACT_MESSAGE,
        "time": get_unix_time_str(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "online"
        },
        "to": to,
        "msg": message,
    }
    return message_dict


def print_help():
    print('Type: m - start a new message, q - quit')


def read_thread(s, name):
    while True:
        try:
            answer = get_message(s)
            logger.debug(f'Got an answer from server: {answer}')
            if 'action' in answer and answer['action'] == 'msg' and 'user' in answer and 'to' in answer and \
                    answer['to'] == name:
                print(f'NEW | From {answer["user"]["account_name"]} | {answer["msg"]}')
            else:
                print(answer)
        except ValueError as e:
            print(e)


def write_thread(s, name):
    print_help()
    while True:
        user_input = input(f"-> ")
        if user_input == 'm':
            new_message = input('Enter text message: ')
            to = input('Enter receiver\'s name: ')

            message = create_message(new_message, to, name)
            print(f'SENT | To {to} | {new_message}')
            logger.debug(f'Created message: {message}, sending...')
            send_message(s, message)
        else:
            break


def main():
    parser = argparse.ArgumentParser(description='A client')
    parser.add_argument("address", help='Server\'s address. Default: 127.0.0.1', nargs='?', default=HOST)
    parser.add_argument("port", help='Server\'s port. Default: 7777', nargs='?', default=PORT)
    parser.add_argument('-n', dest='name', default='guest', required=False)
    args = parser.parse_args()
    logger.debug(f'Args: {args.address}, {args.port} {args.name}')
    with socket(AF_INET, SOCK_STREAM) as s:
        host = args.address
        port = int(args.port)
        try:
            s.connect((host, port))
            logger.debug(f'Connected to {host}:{port}')
            send_message(s, create_presence(args.name))
            answer = get_message(s)
            handle_answer(answer)
            print(f'Hello, client {args.name}!')
            print('Your address is', s.getsockname())
        except ConnectionRefusedError:
            logger.error('Can\'t connect to a server')
        except Exception as e:
            logger.exception('Error occured by attempting to log in')
            logger.error(e)
        else:
            reading = threading.Thread(None, target=read_thread, args=(s, args.name))
            reading.daemon = True
            reading.start()

            writing = threading.Thread(None, target=write_thread, args=(s, args.name))
            writing.daemon = True
            writing.start()

            while True:
                time.sleep(1)
                if reading.is_alive() and writing.is_alive():
                    continue
                break


if __name__ == '__main__':
    main()
