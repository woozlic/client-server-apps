from socket import AF_INET, SOCK_STREAM, socket
import json
import argparse

from common.variables import PORT, BYTES_RECV_SIZE, ACT_PRESENCE
from common.utils import get_unix_time_str, send_message, get_message


def handle_answer(message):
    RESPONSES = {
        200: 'All right'
    }
    print(message)
    resp = message['response']
    if resp in RESPONSES:
        print(RESPONSES[resp])


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


def main():
    parser = argparse.ArgumentParser(description='A client')
    parser.add_argument("address", help='Server\'s address. Required')
    parser.add_argument("port", help='Server\'s port. Default: 7777', nargs='?', default=PORT)
    args = parser.parse_args()
    print(args)
    with socket(AF_INET, SOCK_STREAM) as s:
        host = args.address
        port = int(args.port)
        s.connect((host, port))
        message = create_presence()
        send_message(s, message)
        answer = get_message(s)
        handle_answer(answer)


if __name__ == '__main__':
    main()
