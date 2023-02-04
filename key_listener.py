import pyperclip
from pynput import keyboard
from pynput.keyboard import Controller, Key
import subprocess

pressed = set()
keyb2=Controller()

COMBINATIONS = [
    {
        "keys": [
            # {keyboard.Key.left, keyboard.Key.down},
            {keyboard.Key.ctrl_l, keyboard.Key.down},
        ],
        "command": "notepad",
        "cmd":1
    },
    {
        "keys": [
            {keyboard.Key.cmd, keyboard.KeyCode(char="c")},
            {keyboard.Key.cmd, keyboard.KeyCode(char="C")},
        ],
        "command": "calc",
        "cmd":2
    },
]

def run(s):
    subprocess.Popen(s)
prev=""
pyperclip.copy(prev)
def on_press(key):
    global prev
    pressed.add(key)
    # print(pressed)
    for c in COMBINATIONS:
        for keys in c["keys"]:
            if keys.issubset(pressed):
                if c["cmd"]==1:
                    keyb2.press(Key.ctrl)
                    keyb2.press('c')
                    keyb2.release('c')
                    keyb2.release(Key.ctrl)
                    temp=pyperclip.paste()
                    if prev!=temp:
                        print(temp)
                        prev=temp

def on_release(key):
    if key in pressed:
        pressed.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


