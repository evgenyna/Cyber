"""
HTTP Server Shell

Authors: Barak Gonen, Nir Dweck
Purpose: Provide a basis for Ex. 4

Note: The code is written in a simple way, without classes, log files or
other utilities, for educational purpose

Usage: Fill the missing functions and constants

Updated by: Evgeny Hezi Naftaliev
"""
# TO DO: import modules
import socket
import os

# TO DO: set constants
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 2
WEB_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webroot')
DEFAULT_URL = '/index.html'

CONTENT_TYPES = {
    'html': 'text/html;charset=utf-8',
    'jpg':  'image/jpeg',
    'css':  'text/css',
    'js':   'text/javascript; charset=UTF-8',
    'txt':  'text/plain',
    'ico':  'image/x-icon',
    'gif':  'image/jpeg',
    'png':  'image/png',
}

REDIRECTION_DICTIONARY = {
    '/moved': '/',
}

FORBIDDEN_URIS = {'/forbidden','/f'}
ERROR_URIS = {'/error'}


def get_file_data(file_name):
    """
    Get data from file.

    :param file_name: the name of the file to read
    :return: the file data as bytes
    """
    # TO DO: read the data from the file
    with open(file_name, 'rb') as f:
        return f.read()


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send to client.

    :param resource: the requested URI/resource path (e.g., '/index.html', '/')
    :param client_socket: a socket for the communication with the client
    :return: None (response is sent directly to client_socket)
    """
    # TO DO: add code that given a resource (URL and parameters) generates
    # the proper response
    if resource == '/' or resource == '':
        uri = DEFAULT_URL
    else:
        uri = resource

    # TO DO: check if URL had been redirected, not available or other error code
    # Send 403 Forbidden
    if uri.rstrip('/') in FORBIDDEN_URIS:
        http_header = 'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n'
        client_socket.send(http_header.encode())
        return

    # Send 500 Internal Server Error
    if uri.rstrip('/') in ERROR_URIS:
        http_header = 'HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n'
        client_socket.send(http_header.encode())
        return

    # Send 302 redirection response
    if uri.rstrip('/') in REDIRECTION_DICTIONARY:
        location = REDIRECTION_DICTIONARY[uri.rstrip('/')]
        http_header = (
            'HTTP/1.1 302 Moved Temporarily\r\n'
            'Location: {}\r\n'
            'Content-Length: 0\r\n\r\n'
        ).format(location)
        client_socket.send(http_header.encode())
        return

    # TO DO: check if the file exists relative to WEB_ROOT, send 404 if not
    file_path = os.path.join(WEB_ROOT, uri.lstrip('/'))
    if not os.path.isfile(file_path):
        http_header = 'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'
        client_socket.send(http_header.encode())
        return

    # TO DO: extract requested file type from URL (html, jpg etc)
    ext = uri.rsplit('.', 1)[-1].lower() if '.' in uri else ''

    # TO DO: generate proper HTTP header with Content-Type and Content-Length
    content_type = CONTENT_TYPES.get(ext, 'application/octet-stream')

    data = get_file_data(file_path)

    http_header = (
        'HTTP/1.1 200 OK\r\n'
        'Content-Type: {}\r\n'
        'Content-Length: {}\r\n\r\n'
    ).format(content_type, len(data))

    # http_header should be encoded before sending
    # data encoding depends on its content: text should be encoded, while files shouldn't
    client_socket.send(http_header.encode() + data)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL.

    :param request: the request which was received from the client as a string
    :return: tuple of (is_valid: bool, resource: str) — True if valid HTTP GET request, resource path if valid, empty string if invalid
    """
    # TO DO: write function
    lines = request.split('\r\n')
    if not lines:
        return False, ''
    parts = lines[0].split(' ')
    if len(parts) != 3:
        return False, ''
    method, uri, version = parts
    if method != 'GET':
        return False, ''
    if version != 'HTTP/1.1':
        return False, ''
    return True, uri


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests.

    :param client_socket: the socket for the communication with the client
    :return: None (closes connection after handling or on error/timeout)
    """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        try:
            client_request = client_socket.recv(4096).decode()
        except socket.timeout:
            break
        if not client_request:
            break
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
        else:
            print('Error: Not a valid HTTP request')
            # TO DO: send 400 Bad Request response
            http_header = 'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n'
            client_socket.send(http_header.encode())
            break
    print('Closing connection')


def main():
    """
    Main server entry point.

    Opens a TCP server socket, binds to IP:PORT, and listens for incoming
    client connections. Delegates each connection to handle_client() in a loop.
    Handles socket errors gracefully and ensures cleanup on exit.

    :return: None (runs indefinitely until interrupted or socket error)
    """
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, _ = server_socket.accept()
            try:
                print('New connection received')
                client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                print('received socket exception - ' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
