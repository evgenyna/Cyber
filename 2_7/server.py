"""
Remote technician server.

Author: Evgeny Hezi Naftaliev
"""
import socket
import os
import logging
from protocol import *
import functions

PORT = 20010
IP = '0.0.0.0'
BACKLOG = 5
EXIT_CMD = 'EXIT'
EXIT_REPLY = b'BYE'
LOG_FILE = os.path.join('logs', 'server.log')

CMD_HANDLERS = {
    'dir':             functions.list_directory,
    'del':             functions.delete_file,
    'copy':            functions.copy_file,
    'exe_program':     functions.run_program,
    'take_screenshot': functions.capture_screenshot,
    'send_photo':      functions.send_photo,
    'name':            functions.get_hostname,
}


def setup_logging():
    """
    Ensure log directory exists and configure the logging module.

    :return: None
    """
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format='%(levelname)s | %(asctime)s | %(funcName)s | %(message)s'
    )


def process_client(conn, addr):
    """
    Handle an accepted client connection and process commands.

    :param conn: socket connection object
    :param addr: client address tuple
    :return: None
    """
    logging.info('new connection from ' + str(addr))
    print('connected: ' + str(addr))
    try:
        while True:
            cmd, data = recv_msg(conn)
            if not cmd:
                break
            logging.info(str(addr) + ' -> ' + cmd)

            if cmd == EXIT_CMD:
                send_msg(conn, EXIT_CMD, EXIT_REPLY)
                break
            elif cmd in CMD_HANDLERS:
                result = CMD_HANDLERS[cmd](data)
                send_msg(conn, cmd, result)
            else:
                send_msg(conn, cmd, b'unsupported command: ' + cmd.encode())
    except socket.error as err:
        logging.error('socket error with ' + str(addr) + ': ' + str(err))
        print('client disconnected: ' + str(addr))
    finally:
        conn.close()
        logging.info('closed: ' + str(addr))
        print('closed: ' + str(addr))


def main():
    """
    Start the TCP server and accept incoming connections.

    Binds to `IP:PORT` and delegates clients to `process_client`.
    :return: None
    """
    setup_logging()
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((IP, PORT))
        srv.listen(BACKLOG)
        print('server running on port ' + str(PORT))
        while True:
            conn, addr = srv.accept()
            process_client(conn, addr)
    except socket.error as err:
        logging.error('bind/listen failed: ' + str(err))
        print('failed to start server: ' + str(err))
    finally:
        srv.close()


if __name__ == '__main__':
    main()
