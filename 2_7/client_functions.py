"""
Client-side input and display handlers.
INPUT_MAP[cmd]() -> bytes     payload to send to the server
OUTPUT_MAP[cmd](bytes)        display or save the server response
"""
import os
import logging

SCREENSHOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_screen.jpg')
COMMANDS = ('dir', 'del', 'copy', 'exe_program', 'take_screenshot', 'send_photo', 'name', 'EXIT')
EXIT_RESP = b'BYE'


def input_dir():
    return input('directory to list: ').encode()

def show_dir(data):
    print(data.decode())


def input_del():
    return input('file to delete: ').encode()

def show_del(data):
    print(data.decode())


def input_copy():
    src = input('source file: ')
    dst = input('destination: ')
    return (src + '\n' + dst).encode()

def show_copy(data):
    print(data.decode())


def input_exe_program():
    return input('program full path: ').encode()

def show_exe_program(data):
    print(data.decode())


def input_take_screenshot():
    return b''

def show_take_screenshot(data):
    print(data.decode())


def input_send_photo():
    return b''

def show_send_photo(data):
    if not data.startswith(b'\xff\xd8\xff'):
        print('send_photo failed: ' + data.decode())
        return
    with open(SCREENSHOT_PATH, 'wb') as f:
        f.write(data)
    print('screenshot saved to ' + SCREENSHOT_PATH)


def input_name():
    return b''

def show_name(data):
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
