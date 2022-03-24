import logging
from socket import AF_INET, SOCK_STREAM, socket
import argparse

import json

from common.errors import ReqFieldMissingError, ServerError
from common.variables import PORT, ACT_PRESENCE, HOST, ACT_MESSAGE
from common.utils import get_unix_time_str, send_message, get_message
import log.client_log_config
import sys
from common.decorators import log

logger = logging.getLogger('client')


@log
def handle_answer(message):
    if 'text' in message:
        print(f"{message['from']}: {message['text']}")


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
def create_message(text: str, account_name='guest'):
    message = {
        "action": ACT_MESSAGE,
        "time": get_unix_time_str(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "online"
        },
        "text": text
    }
    return message


def main():

    parser = argparse.ArgumentParser(description='A client')
    parser.add_argument("address", help='Server\'s address. Default: 127.0.0.1', nargs='?', default=HOST)
    parser.add_argument("port", help='Server\'s port. Default: 7777', nargs='?', default=PORT)
    parser.add_argument("-m", dest='mode', help='Mode, [listen | send]. Listen by default', default='listen')
    args = parser.parse_args()
    client_mode = args.mode
    logger.debug(f'Args: {args.address}, {args.port}')
    with socket(AF_INET, SOCK_STREAM) as s:
        host = args.address
        port = int(args.port)
        try:
            s.connect((host, port))
            logger.debug(f'Connected to {host}:{port}')
            message = create_presence()
            logger.debug(f'Created presence: {message}, sending...')
            send_message(s, message)
            answer = get_message(s)
            logger.debug(f'Got an answer from server: {answer}')
            handle_answer(answer)
        except ConnectionRefusedError:
            logger.critical('Can\'t connect to a server')
        except json.JSONDecodeError:
            logger.error('Не удалось декодировать полученную Json строку.')
            sys.exit(1)
        except ServerError as error:
            logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
            sys.exit(1)
        except ReqFieldMissingError as missing_error:
            logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            sys.exit(1)
        else:
            if client_mode == 'send':
                print('SENDING MOD!')
            elif client_mode == 'listen':
                print('LISTENING MOD!')
            while True:
                if client_mode == 'send':
                    try:
                        user_input = input('Enter a message: ')
                        send_message(s, create_message(user_input))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        logger.error(f'Connection to a server {host}:{port} was lost.')
                        sys.exit(1)
                elif client_mode == 'listen':
                    try:
                        handle_answer(get_message(s))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        logger.error(f'Connection to a server {host}:{port} was lost.')
                        sys.exit(1)


if __name__ == '__main__':
    main()
