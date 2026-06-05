"""
Server-side command handlers.
All functions receive bytes and return bytes.
"""
import os
import shutil
import subprocess
import socket as _socket
import logging

try:
    import pyautogui
    _SCREENSHOT_AVAILABLE = True
except ImportError:
    _SCREENSHOT_AVAILABLE = False

SCREENSHOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server_screen.jpg')
OK = b'done'
FAIL = b'failed: '
NOT_FOUND = b'path not found: '

try:
    logging.basicConfig(
        filename='logs/functions.log',
        level=logging.DEBUG,
        format='%(levelname)s | %(asctime)s | %(funcName)s | %(message)s'
    )
except FileNotFoundError:
    os.makedirs('logs')
    logging.basicConfig(
        filename='logs/functions.log',
        level=logging.DEBUG,
        format='%(levelname)s | %(asctime)s | %(funcName)s | %(message)s'
    )


def list_directory(path_bytes):
    """
    List all entries in a directory.
    :param path_bytes: bytes of the directory path
    :return: newline-separated entries as bytes, or error message
    """
    path = path_bytes.decode()
    if not os.path.isdir(path):
        return NOT_FOUND + path_bytes
    entries = os.listdir(path)
    return '\n'.join(os.path.join(path, e) for e in entries).encode()


def delete_file(path_bytes):
    """
    Delete a file at the given path.
    :param path_bytes: bytes of the file path
    :return: OK or error bytes
    """
    path = path_bytes.decode()
    try:
        os.remove(path)
        return OK
    except OSError as err:
        logging.warning(str(err))
        return FAIL + str(err).encode()


def copy_file(paths_bytes):
    """
    Copy src to dst (paths separated by newline in payload).
    :param paths_bytes: bytes with src\\ndst
    :return: OK or error bytes
    """
    try:
        src, dst = paths_bytes.decode().split('\n', 1)
        shutil.copy(src, dst)
        return OK
    except Exception as err:
        logging.warning(str(err))
        return FAIL + str(err).encode()


def run_program(path_bytes):
    """
    Launch a program by its full path.
    :param path_bytes: bytes of the executable path
    :return: OK or error bytes
    """
    path = path_bytes.decode()
    if not os.path.isfile(path):
        return NOT_FOUND + path_bytes
    try:
        subprocess.Popen(path)
        return OK
    except OSError as err:
        logging.warning(str(err))
        return FAIL + str(err).encode()


def capture_screenshot(_):
    """
    Take a screenshot and save it on the server.
    :param _: unused
    :return: OK or error bytes
    """
    if not _SCREENSHOT_AVAILABLE:
        return FAIL + b'pyautogui not installed'
    try:
        img = pyautogui.screenshot()
        img.save(SCREENSHOT_PATH)
        return OK
    except Exception as err:
        logging.warning(str(err))
        return FAIL + str(err).encode()


def send_photo(_):
    """
    Read the saved screenshot and return its bytes.
    :param _: unused
    :return: JPEG image bytes or error bytes
    """
    try:
        with open(SCREENSHOT_PATH, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return FAIL + b'no screenshot found, run take_screenshot first'
    except OSError as err:
        logging.warning(str(err))
        return FAIL + str(err).encode()


def get_hostname(_):
    """
    Return the server's hostname.
    :param _: unused
    :return: hostname as bytes
    """
    return _socket.gethostname().encode()
