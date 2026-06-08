"""
Client-side input and display handlers.

INPUT_MAP[cmd]() -> bytes     payload to send to the server
OUTPUT_MAP[cmd](bytes)        display or save the server response

Author: Evgeny Hezi Naftaliev
"""
import os
import logging

SCREENSHOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_screen.jpg')
COMMANDS = ('dir', 'del', 'copy', 'exe_program', 'take_screenshot', 'send_photo', 'name', 'EXIT')
EXIT_RESP = b'BYE'


def input_dir():
    """
    Prompt for a directory path and return it encoded as bytes.

    :return: directory path as bytes
    """
    return input('directory to list: ').encode()

def show_dir(data):
    """
    Display directory listing received from server.

    :param data: response bytes from server
    """
    print(data.decode())


def input_del():
    """
    Prompt for a file path to delete and return it as bytes.

    :return: file path as bytes
    """
    return input('file to delete: ').encode()

def show_del(data):
    """
    Show deletion result from server.

    :param data: response bytes from server
    """
    print(data.decode())


def input_copy():
    """
    Prompt for source and destination and return both as bytes.

    Payload format: b'src\ndst'
    :return: combined paths as bytes
    """
    src = input('source file: ')
    dst = input('destination: ')
    return (src + '\n' + dst).encode()

def show_copy(data):
    """
    Show copy command result from server.

    :param data: response bytes from server
    """
    print(data.decode())


def input_exe_program():
    """
    Prompt for program full path and return it as bytes.

    :return: executable path as bytes
    """
    return input('program full path: ').encode()

def show_exe_program(data):
    """
    Display result of program execution request.

    :param data: response bytes from server
    """
    print(data.decode())


def input_take_screenshot():
    """
    Return an empty payload for screenshot command.

    :return: empty bytes
    """
    return b''

def show_take_screenshot(data):
    """
    Print result of screenshot capture.

    :param data: response bytes from server
    """
    print(data.decode())


def input_send_photo():
    """
    Return an empty payload for send_photo command.

    :return: empty bytes
    """
    return b''

def show_send_photo(data):
    """
    Save JPEG bytes received from server to SCREENSHOT_PATH.

    :param data: bytes expected to be a JPEG image
    """
    if not data.startswith(b'\xff\xd8\xff'):
        print('send_photo failed: ' + data.decode())
        return
    with open(SCREENSHOT_PATH, 'wb') as f:
        f.write(data)
    print('screenshot saved to ' + SCREENSHOT_PATH)


def input_name():
    """
    Return an empty payload for name command.

    :return: empty bytes
    """
    return b''

def show_name(data):
    """
    Print the server hostname received as bytes.

    :param data: hostname bytes
    """
    print('server hostname: ' + data.decode())


INPUT_MAP = {
    'dir':             input_dir,
    'del':             input_del,
    'copy':            input_copy,
    'exe_program':     input_exe_program,
    'take_screenshot': input_take_screenshot,
    'send_photo':      input_send_photo,
    'name':            input_name,
}

OUTPUT_MAP = {
    'dir':             show_dir,
    'del':             show_del,
    'copy':            show_copy,
    'exe_program':     show_exe_program,
    'take_screenshot': show_take_screenshot,
    'send_photo':      show_send_photo,
    'name':            show_name,
}
