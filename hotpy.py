from functools import reduce
import ctypes
from ctypes import wintypes
import win32con

byref = ctypes.byref
user32 = ctypes.windll.user32

CALLBACKS = []

def create_key_lookup():#{{{
    """Creates Key look up dictionaries, change names as you please"""
    ID2Key = {
                 9: 'Tab',
                 13: 'Return',
                 20: 'Capital',
                 27: 'Escape',
                 32: 'Space',
                 33: 'Prior',
                 34: 'Next',
                 35: 'End',
                 36: 'Home',
                 37: 'Left',
                 38: 'Up',
                 39: 'Right',
                 40: 'Down',
                 44: 'Snapshot',
                 46: 'Delete',
                 48: '0',
                 49: '1',
                 50: '2',
                 51: '3',
                 52: '4',
                 53: '5',
                 54: '6',
                 55: '7',
                 56: '8',
                 57: '9',
                 65: 'A',
                 66: 'B',
                 67: 'C',
                 68: 'D',
                 69: 'E',
                 70: 'F',
                 71: 'G',
                 72: 'H',
                 73: 'I',
                 74: 'J',
                 75: 'K',
                 76: 'L',
                 77: 'M',
                 78: 'N',
                 79: 'O',
                 80: 'P',
                 81: 'Q',
                 82: 'R',
                 83: 'S',
                 84: 'T',
                 85: 'U',
                 86: 'V',
                 87: 'W',
                 88: 'X',
                 89: 'Y',
                 90: 'Z',
                 91: 'Lwin',
                 92: 'Rwin',
                 93: 'App',
                 95: 'Sleep',
                 96: 'Numpad0',
                 97: 'Numpad1',
                 98: 'Numpad2',
                 99: 'Numpad3',
                 100: 'Numpad4',
                 101: 'Numpad5',
                 102: 'Numpad6',
                 103: 'Numpad7',
                 104: 'Numpad8',
                 105: 'Numpad9',
                 106: 'Multiply',
                 107: 'Add',
                 109: 'Subtract',
                 110: 'Decimal',
                 111: 'Divide',
                 112: 'F1',
                 113: 'F2',
                 114: 'F3',
                 115: 'F4',
                 116: 'F5',
                 117: 'F6',
                 118: 'F7',
                 119: 'F8',
                 120: 'F9',
                 121: 'F10',
                 122: 'F11',
                 123: 'F12',
                 144: 'Numlock',
                 160: 'Lshift',
                 161: 'Rshift',
                 162: 'Lcontrol',
                 163: 'Rcontrol',
                 164: 'Lmenu',
                 165: 'Rmenu',
                 186: 'Oem_1',
                 187: 'Oem_Plus',
                 188: 'Oem_Comma',
                 189: 'Oem_Minus',
                 190: 'Oem_Period',
                 191: 'Oem_2',
                 192: 'Oem_3',
                 219: 'Oem_4',
                 220: 'Oem_5',
                 221: 'Oem_6',
                 222: 'Oem_7',
                 1001: 'mouse left', #mouse hotkeys
                 1002: 'mouse right',
                 1003: 'mouse middle',
                 1000: 'mouse move', #single event hotkeys
                 1004: 'mouse wheel up',
                 1005: 'mouse wheel down',
                 win32con.MOD_CONTROL: 'Ctrl', #merged hotkeys
                 win32con.MOD_ALT: 'Alt',
                 win32con.MOD_SHIFT: 'Shift',
                 win32con.MOD_WIN: 'Win'}

    Key2ID = dict(map(lambda x,y: (x,y),ID2Key.values(),ID2Key.keys()))

    return ID2Key, Key2ID#}}}

id_to_key, key_to_id = create_key_lookup()


def register(callback, key, modifiers=None):
    """Register a  hotkey

    keys are given as simple names
    modifiers is a list
    """
    global CALLBACKS

    if modifiers is not None:
        numeric_modifiers = [key_to_id[m] for m in modifiers]
        modifiers_or = reduce(lambda x, y: x | y,
                              numeric_modifiers)
    else:
        modifiers_or = None

    next_id = len(CALLBACKS) + 1
    ret = user32.RegisterHotKey(None, next_id, modifiers_or, key_to_id[key])
    if not ret:
        raise RuntimeError("Could not map hotkey")
    CALLBACKS.append(callback)


def listen():
    """Begin the message loop, waiting for hotkeys"""

    try:
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                callback_id = msg.wParam - 1
                ret = CALLBACKS[callback_id]()
                # Exit if the callback returns false.
                if ret == False:
                    break

            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageA(byref(msg))

    finally:
        user32.UnregisterHotKey(None, 1)

#{{{  Test functions
def handle_f9():
    print("F9 Pressed")

def handle_f8():
    print("F8 Pressed, exiting now!")
    return False

def handle_c_f9():
    print("Control+F9 Pressed")

def test():
    print("Testing, press F9, Ctrl+F9, and F8 to exit")

    register(handle_f9, 'F9')
    register(handle_f8, 'F8')
    register(handle_c_f9, 'F9', ['Ctrl'])
    listen()
#}}}

if __name__ == "__main__":
    test()
