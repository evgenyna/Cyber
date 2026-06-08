"""
Protocol helpers for length-prefixed messaging used by client/server.

Author: Evgeny Hezi Naftaliev
"""

import struct
import logging

PACK_FORMAT = 'I'
HEADER_SIZE = struct.calcsize(PACK_FORMAT)


def send_msg(sock, cmd, data):
    """
    Transmit a command and its payload over the socket.
    :param sock: connected socket
    :param cmd: command name as string
    :param data: command payload as bytes
    :return: None
    """
    header_cmd = struct.pack(PACK_FORMAT, len(cmd))
    header_data = struct.pack(PACK_FORMAT, len(data))
    packet = header_cmd + cmd.encode() + header_data + data
    total_sent = 0
    while total_sent < len(packet):
        total_sent += sock.send(packet[total_sent:])
    logging.debug('packet sent: ' + str(packet))


def read_chunk(sock):
    """
    Read one length-prefixed chunk from the socket.
    :param sock: connected socket
    :return: the chunk data as bytes
    """
    raw_size = b''
    while len(raw_size) < HEADER_SIZE:
        piece = sock.recv(HEADER_SIZE - len(raw_size))
        if piece == b'':
            return b''
        raw_size += piece
    chunk_size = struct.unpack(PACK_FORMAT, raw_size)[0]
    logging.debug('expecting ' + str(chunk_size) + ' bytes')
    chunk = b''
    while len(chunk) < chunk_size:
        piece = sock.recv(chunk_size - len(chunk))
        if piece == b'':
            break
        chunk += piece
    return chunk


def recv_msg(sock):
    """
    Receive a command and its payload from the socket.
    :param sock: connected socket
    :return: (command string, payload bytes)
    """
    cmd = read_chunk(sock).decode()
    payload = read_chunk(sock)
    return cmd, payload
