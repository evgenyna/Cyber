"""
Remote technician client.

Author: Evgeny Hezi Naftaliev
"""
import socket
from protocol import *
import client_functions

SERVER_IP = '127.0.0.1'
SERVER_PORT = 20010


def print_menu():
    """
    Print the available commands supported by the client.

    Uses the `COMMANDS` tuple from `client_functions`.
    """
    print('available commands: ' + ' | '.join(client_functions.COMMANDS))


def main():
    """
    Create a TCP connection to the server and interactively send commands.

    The function connects to `SERVER_IP:SERVER_PORT`, reads user input,
    sends commands using `protocol.send_msg` and displays responses.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        print('connected to ' + SERVER_IP + ':' + str(SERVER_PORT))
        print_menu()

        while True:
            cmd = input('> ').strip()
            if cmd not in client_functions.COMMANDS:
                print('unknown command')
                print_menu()
                continue

            if cmd == 'EXIT':
                send_msg(sock, 'EXIT', b'')
                _, reply = recv_msg(sock)
                print(reply.decode())
                break

            payload = client_functions.INPUT_MAP[cmd]()
            send_msg(sock, cmd, payload)
            _, response = recv_msg(sock)
            client_functions.OUTPUT_MAP[cmd](response)

    except socket.error as err:
        print('connection error: ' + str(err))
    finally:
        sock.close()


if __name__ == '__main__':
    main()
